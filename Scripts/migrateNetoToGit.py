# Script migrating Neto data set from SVN to github
# To run you will need github token
import requests
import csv
import os

csvPath = './dataset_bugfix_bic.csv'

with open(os.path.realpath(os.path.join(os.path.dirname(__file__), './token.txt'))) as tokenFile:
    token = tokenFile.readline()

headers = None if token == r'INSERT_GITHUB_TOKEN_HERE' else {
    'Authorization': 'token {}'.format(token)}


def buildRepoUrl(repo, page):
    return f'https://api.github.com/repos/{repo}/commits?per_page=100&page={page}'


def fetchAllCommits(repo, log=True):
    page = 1
    allCommits = []
    commitsPage = fetchCommitsPage(repo, page=page)
    while len(commitsPage) > 0:
        if log:
            print(f'Fetching page {page}')
        allCommits += commitsPage
        page = page + 1
        commitsPage = fetchCommitsPage(repo, page=page)

    return allCommits


def createCommitDict(commits):
    for i in commits:
        pass


def fetchCommitsPage(repo, page):
    url = buildRepoUrl(repo, page=page)
    try:
        r = requests.get(url=url, headers=headers)
        return r.json()
    except Exception as e:
        print(e)
        return None


def getGitSha(shaMsgPairs, svnrev):
    for p in shaMsgPairs:
        if f'trunk@{svnrev}' in p[1]:
            return p[0]

    return None


data = []
with open(csvPath, newline='', encoding="utf-8-sig") as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    readerList = list(reader)

    labels = None
    for rowId in range(1):
        labels = readerList[rowId]
    for rowId in range(1, len(readerList)):
        z = zip(labels, readerList[rowId])
        data.append(dict(z))


langDataIter = filter(lambda x: x['project'] == 'commons-lang', data)
fixIntrodPairIter = map(lambda x: (x['bugfix_commit'],
                                   x['bugintroducingchange_commit'], x['pathbugfix']), langDataIter)


commitsIterLang = list(map(lambda c: (
    c['sha'], c['commit']['message']), fetchAllCommits('apache/commons-lang', log=False)))
commitsIterMath = list(map(lambda c: (
    c['sha'], c['commit']['message']), fetchAllCommits('apache/commons-math', log=False)))

mismatchCount = 0
with open('out.csv', 'w', encoding='utf-8') as f:
    keys = ','.join(data[0].keys())
    f.write(f'{keys}\n')
    for i in data:
        if i['project'] == 'commons-lang':
            i['bugfix_commit'] = getGitSha(commitsIterLang, i['bugfix_commit'])
            i['bugintroducingchange_commit'] = getGitSha(
                commitsIterLang, i['bugintroducingchange_commit'])
            w = ','.join([x for key, x in i.items()])
            f.write(f'{w}\n')
        elif i['project'] == 'commons-math':
            i['bugfix_commit'] = getGitSha(commitsIterMath, i['bugfix_commit'])
            i['bugintroducingchange_commit'] = getGitSha(
                commitsIterMath, i['bugintroducingchange_commit'])
            if i['bugfix_commit'] == None or i['bugintroducingchange_commit'] == None:
                mismatchCount += 1
            else:
                w = ','.join([x for key, x in i.items()])
                f.write(f'{w}\n')
        elif i['project'] in ['mockito', 'joda-time', 'closure-compiler']:
            w = ','.join([x for key, x in i.items()])
            f.write(f'{w}\n')

    print(f'Mach not found for: {mismatchCount}')
