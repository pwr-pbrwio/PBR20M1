from toolz.curried import pipe, map, filter, get
import csv
import json
import os
import argparse

netoPath = os.path.join(os.path.dirname(__file__), 'git_neto.csv')
unleashPath = './results/fix_and_introducers_pairs.json'


def main(repoName):
    # Read json file into 'szzData' variable
    with open(unleashPath, 'r', encoding='utf-8') as f:
        szzData = json.load(f)

    # remove repetitions
    szzData = [tuple(x) for x in szzData]
    szzData = list(dict.fromkeys(szzData))

    # Read csv file into 'netoData' variable
    netoData = []
    with open(netoPath, newline='', encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        readerList = list(reader)

        labels = None
        for rowId in range(1):
            labels = readerList[rowId]
        for rowId in range(1, len(readerList)):
            # filter repository

            z = zip(labels, readerList[rowId])
            d = dict(z)
            if d['project'] == repoName:
                netoData.append(d)

    # remove repetitions
    netoData = [(x['bugfix_commit'], x['bugintroducingchange_commit'],
                 x['pathbugfix']) for x in netoData]
    netoData = list(dict.fromkeys(netoData))

    notMatched = netoData.copy()
    notMatchedWithFile = netoData.copy()
    notMatchedFixes = netoData.copy()

    # Iterate over szz results
    for unl in szzData:
        notMatchedFixes = pipe(
            notMatchedFixes, filter(lambda x: not (x[0] == unl[0])), list)

        notMatched = pipe(
            notMatched, filter(lambda x: not (x[0] == unl[0] and x[1] == unl[1])), list)

        if len(unl) > 2:
            notMatchedWithFile = pipe(
                notMatchedWithFile, filter(lambda x: not (x[0] == unl[0] and x[1] == unl[1] and x[2].endswith(unl[2]))), list)

    acc = (len(netoData) - len(notMatched))
    accWFile = (len(netoData) - len(notMatchedWithFile))

    # print(f'In both without matching file: {acc}')
    print(f'In both: {accWFile}')
    print(f'In data set: {len(netoData)}')

    # Test how many matches in ra-unleashed are correct
    notMatched = szzData.copy()
    notMatchedWithFile = szzData.copy()

    for res in netoData:
        notMatched = pipe(
            notMatched, filter(lambda x: not (x[0] == res[0] and x[1] == res[1])), list)

        if len(szzData[0]) > 2:
            notMatchedWithFile = pipe(
                notMatchedWithFile, filter(lambda x: not (x[0] == res[0] and x[1] == res[1] and res[2].endswith(x[2]))), list)

    acc = (len(szzData) - len(notMatched))
    accWFile = (len(szzData) - len(notMatchedWithFile))

    print(f'In results: {len(szzData)}')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="""Convert a git log output to json.""")
    parser.add_argument('--repoName', type=str,
                        help="Repository name.")

    args = parser.parse_args()
    if args.repoName == None:
        print('Usage: python script.py --repoName=name')
        exit(1)
    main(args.repoName)
