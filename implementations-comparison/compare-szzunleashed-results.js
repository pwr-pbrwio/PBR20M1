const fse = require("fs-extra");

const REPO_NAME = "unami-unleashed";
const FIRST_UNLEASHEDSZZ_RESULTS_JSON_FILE =
  "./unami-compare-unleashed/first.json";
const SECOND_UNLEASHEDSZZ_RESULTS_JSON_FILE =
  "./unami-compare-unleashed/second.json";

const FAKE_INDUCING_COMMITS = [
  "d47fec240c633b061a3ae9351f8199e8785261b4",
  "d522432b79044740831a132d8b92e7dab5477444",
  "f3f9e9b02c101973da0ed1a51e5dd60b83e5bc65",
  "4224c83d42502f37c781efe4108198b10f9075dd",
  "7a28a2d05733714850bd7e51a98fc97c42e47103",
  "774228b4c6d5e6f8ec239bc9a3d8f09ca7bfa51b",
  "e1498d8c4f0d6273c30569df772f9a9ac9001e85",
];

const FAKE_FIXING_COMMITS = [
  "4224c83d42502f37c781efe4108198b10f9075dd",
  "586db1262d973fda630f04972093aaaf0bf54414",
  "d45a94e4a366aebc3d666ace480a0d73040ee818",
  "f3f9e9b02c101973da0ed1a51e5dd60b83e5bc65",
  "3eb7299f4fad1fd95c13c81c7b67cdf2cc86b93d",
];

const compareImplementations = async () => {
  const {
    firstUnleashedSZZResults,
    secondUnleashedSZZResults,
  } = await readData();
  const unleashedSZZFirstTransformedResults = convertUnleashedSZZCommitArrayToObjects(
    firstUnleashedSZZResults
  );
  const unleashedSZZSecondTransformedResults = convertUnleashedSZZCommitArrayToObjects(
    secondUnleashedSZZResults
  );

  performComparison(
    unleashedSZZFirstTransformedResults,
    unleashedSZZSecondTransformedResults
  );
  // performDatasetAnalysis('openszz', unleashedSZZFirstTransformedResults, FAKE_INDUCING_COMMITS, FAKE_FIXING_COMMITS);
  // performDatasetAnalysis('unleashedszz', unleashedSZZTransformedResults, FAKE_INDUCING_COMMITS, FAKE_FIXING_COMMITS);
};

const performDatasetAnalysis = (
  datasetName,
  dataset,
  fakeInducingCommits,
  fakeFixingCommits
) => {
  const resultsWithoutFakeInducingCommits = filterOutCommits(
    dataset,
    "bugInducingId",
    fakeInducingCommits
  );
  const resultsWithoutFakeFixingCommits = filterOutCommits(
    dataset,
    "bugFixingId",
    fakeFixingCommits
  );
  const resultsWithoutFakeCommits = filterOutCommits(
    resultsWithoutFakeInducingCommits,
    "bugFixingId",
    fakeFixingCommits
  );
  const resultsWithoutFakeCommitsAndDuplicates = getUniquePairs(
    resultsWithoutFakeCommits
  );
  const bestFixersMap = getBestFixers(resultsWithoutFakeCommitsAndDuplicates);

  console.log(`##### ${datasetName} #####`);
  console.log(`Results count: ${dataset.length}`);
  console.log(
    `Results count without fake inducing commits: ${resultsWithoutFakeInducingCommits.length}`
  );
  console.log(
    `Results count without fake fixing commits: ${resultsWithoutFakeFixingCommits.length}`
  );
  console.log(
    `Results count without fake commits: ${resultsWithoutFakeCommits.length}`
  );
  console.log(
    `Results count without fake commits and duplicates: ${resultsWithoutFakeCommitsAndDuplicates.length}`
  );
  console.log("\n");

  fse.outputFileSync(
    `./results-${REPO_NAME}/${datasetName}/results-without-fake-inducing-commits.json`,
    JSON.stringify(resultsWithoutFakeInducingCommits, null, "\t")
  );
  fse.outputFileSync(
    `./results-${REPO_NAME}/${datasetName}/results-without-fake-fixing-commits.json`,
    JSON.stringify(resultsWithoutFakeFixingCommits, null, "\t")
  );
  fse.outputFileSync(
    `./results-${REPO_NAME}/${datasetName}/results-without-fake-commits.json`,
    JSON.stringify(resultsWithoutFakeCommits, null, "\t")
  );
  fse.outputFileSync(
    `./results-${REPO_NAME}/${datasetName}/results-without-fake-commits-and-duplicates.json`,
    JSON.stringify(resultsWithoutFakeCommitsAndDuplicates, null, "\t")
  );
  fse.outputFileSync(
    `./results-${REPO_NAME}/${datasetName}/best-fixers.json`,
    JSON.stringify([...bestFixersMap], null, "\t")
  );
};

const performComparison = (openSZZResults, unleashedSZZTransformedResults) => {
  const matchingPairs = getMatchingPairs(
    openSZZResults,
    unleashedSZZTransformedResults
  );

  const diffPairs = getDiffPairs(
    matchingPairs,
    openSZZResults,
    unleashedSZZTransformedResults
  );
  const uniqueMatchingPairs = getUniquePairs(matchingPairs);

  saveResults(matchingPairs, uniqueMatchingPairs, diffPairs);
};

const getDiffPairs = (
  matchingPairs,
  openSZZResults,
  unleashedSZZTransformedResults
) => {
  return unleashedSZZTransformedResults.filter(
    (result) =>
      !matchingPairs.find(
        (unleashedRes) =>
          result.bugFixingId === unleashedRes.bugFixingId &&
          result.bugInducingId === unleashedRes.bugInducingId
      )
  );
};

const getBestFixers = (dataset) => {
  const bestFixersMap = new Map();
  dataset.forEach((record) => {
    if (!bestFixersMap.has(record.bugFixingId)) {
      bestFixersMap.set(record.bugFixingId, 1);
    } else {
      bestFixersMap.set(
        record.bugFixingId,
        bestFixersMap.get(record.bugFixingId) + 1
      );
    }
  });
  return bestFixersMap;
};

const filterOutCommits = (dataset, key, commits) => {
  return dataset.filter((record) => !commits.includes(record[key]));
};

const saveResults = (matchingPairs, uniqueMatchingPairs, diffPairs) => {
  console.log("##### Comparison results #####");
  console.log(`Matching pairs count: ${matchingPairs.length}`);
  console.log(`Matching unique pairs count: ${uniqueMatchingPairs.length}`);
  console.log(`Diff pairs count: ${diffPairs.length}`);

  console.log("\n");

  fse.outputFileSync(
    `./results-${REPO_NAME}/matching-unique-pairs.json`,
    JSON.stringify(uniqueMatchingPairs, null, "\t")
  );
  fse.outputFileSync(
    `./results-${REPO_NAME}/matching-pairs.json`,
    JSON.stringify(matchingPairs, null, "\t")
  );
  fse.outputFileSync(
    `./results-${REPO_NAME}/diff-pairs.json`,
    JSON.stringify(diffPairs, null, "\t")
  );
};

const getUniquePairs = (pairs) => {
  const uniquePairsMap = new Map();
  pairs.forEach((pair) =>
    uniquePairsMap.set(pair.bugFixingId + pair.bugInducingId, {
      ...pair,
    })
  );

  return Array.from(uniquePairsMap.values());
};

const getMatchingPairs = (openSZZResults, unleashedSZZResults) => {
  return openSZZResults.filter((result) =>
    unleashedSZZResults.find(
      (unleashedRes) =>
        result.bugFixingId === unleashedRes.bugFixingId &&
        result.bugInducingId === unleashedRes.bugInducingId
    )
  );
};

const convertUnleashedSZZCommitArrayToObjects = (unleashedSZZResults) => {
  return unleashedSZZResults.map((pair) => {
    return {
      bugFixingId: pair[0],
      bugInducingId: pair[1],
      path: pair[2],
    };
  });
};

const readData = async () => {
  const firstUnleashedSZZResultsPromise = loadJSONFile(
    FIRST_UNLEASHEDSZZ_RESULTS_JSON_FILE
  );
  const secondUnleashedSZZResultsPromise = loadJSONFile(
    SECOND_UNLEASHEDSZZ_RESULTS_JSON_FILE
  );
  const [
    firstUnleashedSZZResults,
    secondUnleashedSZZResults,
  ] = await Promise.all([
    firstUnleashedSZZResultsPromise,
    secondUnleashedSZZResultsPromise,
  ]);
  return {
    firstUnleashedSZZResults,
    secondUnleashedSZZResults,
  };
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

compareImplementations();
