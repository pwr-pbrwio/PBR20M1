const fs = require('fs');

const OPENSZZ_RESULTS_JSON_FILE = './commons-bcel-data/openszz.json';
const UNLEASHEDSZZ_RESULTS_JSON_FILE = './commons-bcel-data/unleashedszz.json';

const FAKE_INDUCING_COMMITS = [
  'd47fec240c633b061a3ae9351f8199e8785261b4',
  'd522432b79044740831a132d8b92e7dab5477444',
  'f3f9e9b02c101973da0ed1a51e5dd60b83e5bc65',
  '4224c83d42502f37c781efe4108198b10f9075dd',
  '7a28a2d05733714850bd7e51a98fc97c42e47103',
  '774228b4c6d5e6f8ec239bc9a3d8f09ca7bfa51b',
  'e1498d8c4f0d6273c30569df772f9a9ac9001e85',
];

const FAKE_FIXING_COMMITS = [
  '4224c83d42502f37c781efe4108198b10f9075dd',
  '586db1262d973fda630f04972093aaaf0bf54414',
  'd45a94e4a366aebc3d666ace480a0d73040ee818',
  'f3f9e9b02c101973da0ed1a51e5dd60b83e5bc65',
  '3eb7299f4fad1fd95c13c81c7b67cdf2cc86b93d',
];

const compareImplementations = async () => {
  const { openSZZResults, unleashedSZZResults } = await readData();
  const unleashedSZZTransformedResults = convertUnleashedSZZCommitArrayToObjects(unleashedSZZResults);

  performComparison(openSZZResults, unleashedSZZTransformedResults);
  performDatasetAnalysis('openszz', openSZZResults, FAKE_INDUCING_COMMITS, FAKE_FIXING_COMMITS);
  performDatasetAnalysis('unleashedszz', unleashedSZZTransformedResults, FAKE_INDUCING_COMMITS, FAKE_FIXING_COMMITS);
};

const performDatasetAnalysis = (datasetName, dataset, fakeInducingCommits, fakeFixingCommits) => {
  const resultsWithoutFakeInducingCommits = filterOutCommits(dataset, 'bugInducingId', fakeInducingCommits);
  const resultsWithoutFakeFixingCommits = filterOutCommits(dataset, 'bugFixingId', fakeFixingCommits);
  const resultsWithoutFakeCommits = filterOutCommits(
    resultsWithoutFakeInducingCommits,
    'bugFixingId',
    fakeFixingCommits
  );
  const resultsWithoutFakeCommitsAndDuplicates = getUniquePairs(resultsWithoutFakeCommits);
  const bestFixersMap = getBestFixers(resultsWithoutFakeCommitsAndDuplicates);

  console.log(`##### ${datasetName} #####`);
  console.log(`Results count: ${dataset.length}`);
  console.log(`Results count without fake inducing commits: ${resultsWithoutFakeInducingCommits.length}`);
  console.log(`Results count without fake fixing commits: ${resultsWithoutFakeFixingCommits.length}`);
  console.log(`Results count without fake commits: ${resultsWithoutFakeCommits.length}`);
  console.log(`Results count without fake commits and duplicates: ${resultsWithoutFakeCommitsAndDuplicates.length}`);
  // console.log('Further calculations performed on the set without fake commits and duplicates');
  console.log('\n');

  fs.writeFileSync(
    `./results/${datasetName}/results-without-fake-inducing-commits.json`,
    JSON.stringify(resultsWithoutFakeInducingCommits)
  );
  fs.writeFileSync(
    `./results/${datasetName}/results-without-fake-fixing-commits.json`,
    JSON.stringify(resultsWithoutFakeFixingCommits)
  );
  fs.writeFileSync(
    `./results/${datasetName}/results-without-fake-commits.json`,
    JSON.stringify(resultsWithoutFakeCommits)
  );
  fs.writeFileSync(
    `./results/${datasetName}/results-without-fake-commits-and-duplicates.json`,
    JSON.stringify(resultsWithoutFakeCommitsAndDuplicates)
  );
  fs.writeFileSync(`./results/${datasetName}/best-fixers.json`, JSON.stringify([...bestFixersMap]));
};

const performComparison = (openSZZResults, unleashedSZZTransformedResults) => {
  const matchingPairs = getMatchingPairs(openSZZResults, unleashedSZZTransformedResults);
  const uniqueMatchingPairs = getUniquePairs(matchingPairs);

  saveResults(matchingPairs, uniqueMatchingPairs);
};

const getBestFixers = (dataset) => {
  const bestFixersMap = new Map();
  dataset.forEach((record) => {
    if (!bestFixersMap.has(record.bugFixingId)) {
      bestFixersMap.set(record.bugFixingId, 1);
    } else {
      bestFixersMap.set(record.bugFixingId, bestFixersMap.get(record.bugFixingId) + 1);
    }
  });
  return bestFixersMap;
};

const filterOutCommits = (dataset, key, commits) => {
  return dataset.filter((record) => !commits.includes(record[key]));
};

const saveResults = (matchingPairs, uniqueMatchingPairs) => {
  console.log('##### Comparison results #####');
  console.log(`Matching pairs count: ${matchingPairs.length}`);
  console.log(`Matching unique pairs count: ${uniqueMatchingPairs.length}`);
  console.log('\n');

  fs.writeFileSync('./results/matching-unique-pairs.json', JSON.stringify(uniqueMatchingPairs));
  fs.writeFileSync('./results/matching-pairs.json', JSON.stringify(matchingPairs));
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
        result.bugFixingId === unleashedRes.bugFixingId && result.bugInducingId === unleashedRes.bugInducingId
    )
  );
};

const convertUnleashedSZZCommitArrayToObjects = (unleashedSZZResults) => {
  return unleashedSZZResults.map((pair) => {
    return {
      bugFixingId: pair[0],
      bugInducingId: pair[1],
    };
  });
};

const readData = async () => {
  const openSZZResultsPromise = loadJSONFile(OPENSZZ_RESULTS_JSON_FILE);
  const unleashedSZZResultsPromise = loadJSONFile(UNLEASHEDSZZ_RESULTS_JSON_FILE);
  const [openSZZResults, unleashedSZZResults] = await Promise.all([openSZZResultsPromise, unleashedSZZResultsPromise]);
  return {
    openSZZResults,
    unleashedSZZResults,
  };
};

const loadJSONFile = (filepath) => {
  return new Promise((resolve, reject) => {
    fs.readFile(filepath, 'utf8', (err, content) => {
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
