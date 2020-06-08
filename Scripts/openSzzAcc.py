from toolz.curried import pipe, map, filter, get
import os
import csv
import argparse

netoPath = os.path.join(os.path.dirname(__file__), 'git_neto.csv')
openPath = './BugInducingCommits.csv'


def main(repoName):

    openData = []
    with open(openPath, newline='', encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='|')
        readerList = list(reader)

        labels = None
        for rowId in range(1):
            labels = readerList[rowId]
        for rowId in range(1, len(readerList)):
            z = zip(labels, readerList[rowId])
            if len(readerList[rowId]) > 1:
                d = dict(z)
                openData.append(d)

    # remove repetitions
    openData = [(x['bugFixingId'], x['bugInducingId'],
                 x['bugFixingfileChanged']) for x in openData]
    openData = list(dict.fromkeys(openData))

    # Read csv file into 'netoData' variable
    netoData = []
    with open(netoPath, newline='', encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        readerList = list(reader)

        labels = None
        for rowId in range(1):
            labels = readerList[rowId]
        for rowId in range(1, len(readerList)):
            z = zip(labels, readerList[rowId])
            d = dict(z)
            if d['project'] == repoName:
                netoData.append(d)

    # remove repetitions
    netoData = [(x['bugfix_commit'], x['bugintroducingchange_commit'],
                 x['pathbugfix']) for x in netoData]
    netoData = list(dict.fromkeys(netoData))

    # Filter open data for neto fixes
    netoFixes = pipe(netoData, map(lambda x: x[0]), list)
    openData = pipe(openData, filter(lambda x: x[0] in netoFixes), list)

    notMatched = netoData.copy()
    notMatchedWithFile = netoData.copy()
    notMatchedFixes = netoData.copy()

    # Iterate over szz results
    for unl in openData:
        notMatchedFixes = pipe(
            notMatchedFixes, filter(lambda x: not (x[0] == unl[0])), list)

        notMatched = pipe(
            notMatched, filter(lambda x: not (x[0] == unl[0] and x[1] == unl[1])), list)

        if len(unl) > 2:
            notMatchedWithFile = pipe(
                notMatchedWithFile, filter(lambda x: not (x[0] == unl[0] and x[1] == unl[1] and x[2].endswith(unl[2]))), list)

    acc = (len(netoData) - len(notMatched))
    accWFile = (len(netoData) - len(notMatchedWithFile))
    accFixes = (len(netoData) - len(notMatchedFixes))

    print(f'fixes matched: {accFixes}')
    print(f'acc: {acc}')
    print(f'acc with file: {accWFile}')
    print(f'size: {len(netoData)}')

    # Test how many matches in ra-unleashed are correct
    notMatched = openData.copy()
    notMatchedWithFile = openData.copy()

    for res in netoData:
        notMatched = pipe(
            notMatched, filter(lambda x: not (x[0] == res[0] and x[1] == res[1])), list)

        if len(openData) > 0 and len(openData[0]) > 2:
            notMatchedWithFile = pipe(
                notMatchedWithFile, filter(lambda x: not (x[0] == res[0] and x[1] == res[1] and res[2].endswith(x[2]))), list)

    acc = (len(openData) - len(notMatched))
    accWFile = (len(openData) - len(notMatchedWithFile))

    print()
    print('Test how many in openSzz are matched')
    print(f'acc: {acc}')
    print(f'acc with file: {accWFile}')
    print(f'size: {len(openData)}')


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
