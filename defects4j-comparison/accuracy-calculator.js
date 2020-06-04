const fse = require("fs-extra");
const csv = require("csvtojson");

const PROJECT_NAME = "commons-math";
const DATA_INPUT_FILE = "./fix_and_introducers_pairs.json";
const DEFECTS4J_INPUT_FILE = "./d4j.csv";

const main = async () => {
  const [szzResults, bugDb] = await Promise.all([
    getSzzResults(DATA_INPUT_FILE),
    getDefects4jData(DEFECTS4J_INPUT_FILE),
  ]);

  const uniqueSzzResults = filterDuplicatedPairs(szzResults);

  const matchingPairs = getMatchingPairs(uniqueSzzResults, bugDb);
  const szzFixes = szzResults.map(b => b.bugFixCommitId);
  const d4jFixes = bugDb.map(b => b.bugfix_commit);

  let c = 0;
  let c2 = 0;
  console.log(szzResults);
  
  // for (let i of szzFixes) {
  //   console.log(i);
    
  //   if (d4jFixes.includes(i)) {
  //     c++;
  //     console.log(i);
  //     const si = szzFixes.indexOf(i);
  //     const di = d4jFixes.indexOf(i);
  //     // console.log(si, di);
  //     console.log(szzResults[si].bugIntroducerCommitId, bugDb[di].bugintroducingchange_commit);
  //   }
  // }
  // console.log(c);
  // console.log(c2);
  for (let i of szzResults) {
    const fa = bugDb.filter(b => b.bugfix_commit == i.bugFixCommitId);
    console.log(fa);
    console.log(i.bugIntroducerCommitId);
  }
};

const calculateAccuracy = (matchedCasesCount, allCasesCount) =>
  matchedCasesCount / allCasesCount;

const filterBugsForProject = (bugDatabase, projectName) =>
  bugDatabase.filter((record) => record.project === projectName);

const getMatchingPairs = (szzResults, bugDatabase) =>
  bugDatabase.filter((record) =>
    szzResults.some(
      (result) =>
        // record.bugintroducingchange_commit === result.bugIntroducerCommitId &&
        record.bugfix_commit === result.bugFixCommitId
    )
  );

const filterDuplicatedPairs = (pairs) => {
  const uniquePairsMap = new Map();
  pairs.forEach((pair) =>
    uniquePairsMap.set(pair.bugFixCommitId + pair.bugIntroducerCommitId, {
      ...pair,
    })
  );

  return Array.from(uniquePairsMap.values());
};

const getSzzResults = async (path) => {
  const inputData = await loadJSONFile(path);
  return convertArraysArrayToObjectsArray(inputData);
};

const getDefects4jData = (csvFilePath) => {
  return csv().fromFile(csvFilePath);
};

const convertArraysArrayToObjectsArray = (data) => {
  return data.map((pair) => {
    return {
      bugFixCommitId: pair[0],
      bugIntroducerCommitId: pair[1],
      path: pair[2],
    };
  });
};

const loadJSONFile = (filepath) => {
  return new Promise((resolve, reject) => {
    fse.readFile(filepath, "utf8", (err, content) => {
      if (err) {
        reject(err);
      } else {
        try {
          resolve(JSON.parse(content));
        } catch (err) {
          reject(err);
        }
      }
    });
  });
};

main();
