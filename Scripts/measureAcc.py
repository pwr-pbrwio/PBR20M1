from toolz.curried import pipe, map, filter, get
import csv
import json
import os
import argparse

netoPath = os.path.dirname(__file__) + '/git_neto.csv'
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

    # Iterate over szz results
    for unl in szzData:

        notMatched = pipe(
            notMatched, filter(lambda x: not (x[0] == unl[0] and x[1] == unl[1])), list)

        if len(unl) > 2:
            notMatchedWithFile = pipe(
                notMatchedWithFile, filter(lambda x: not (x[0] == unl[0] and x[1] == unl[1] and x[2].endswith(unl[2]))), list)

    acc = (len(netoData) - len(notMatched)) / len(netoData)
    accWFile = (len(netoData) - len(notMatchedWithFile)) / len(netoData)

    print(f'acc: {acc}')
    print(f'acc with file: {accWFile}')


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
