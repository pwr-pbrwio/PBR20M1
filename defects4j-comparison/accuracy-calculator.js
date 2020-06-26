const fse = require("fs-extra");
const csv = require("csvtojson");

const DATA_INPUT_FILE = "./data/input/commons-compress-d3.json";
const DEFECTS4J_INPUT_FILE = "./bugs_dataset.csv";

const main = async () => {
  const [szzResults, bugDb] = await Promise.all([
    getSzzResults(DATA_INPUT_FILE),
    getDefects4jData(DEFECTS4J_INPUT_FILE),
  ]);

  const uniqueSzzResults = filterDuplicatedPairs(szzResults);

  const matchedPairs = getMatchingPairs(szzResults, bugDb);
  const accuracy = calculateAccuracy(
    matchedPairs.length,
    uniqueSzzResults.length
  );
  console.log({ matchedPairs: matchedPairs.length });
  console.log({ accuracy });
};

const calculateAccuracy = (matchedCasesCount, allCasesCount) =>
  matchedCasesCount / allCasesCount;

const filterBugsForProject = (bugDatabase, projectName) =>
  bugDatabase.filter((record) => record.project === projectName);

const getMatchingPairs = (szzResults, bugDatabase) =>
  bugDatabase.filter((record) =>
    szzResults.some(
      (result) =>
        record.bugintroducingchange_commit === result.bugIntroducerCommitId &&
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
