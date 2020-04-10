import csv
import requests
import time


def get(url):
    r = requests.get(url, allow_redirects=False)
    if r.status_code == 200:
        return True
    elif r.status_code == 429:
        print(429)
        time.sleep(0.5)
        get(url)
    else:
        return False


data = []
with open(r"MLCQ.csv", newline='', encoding="utf-8-sig") as csvFile:
    reader = csv.reader(csvFile, delimiter=',', quotechar='|')
    readerList = list(reader)

    labels = None
    for rowId in range(1):
        labels = readerList[rowId]
    for rowId in range(1, len(readerList)):
        z = zip(labels, readerList[rowId])
        data.append(dict(z))

repositoryLinks = []
for rowId in range(0, len(data)):
    link = data[rowId]['link'].split('/blob/')[0]
    if link.startswith('https'):
        repositoryLinks.append(link)

# remove duplicate repositories
repositoryLinks = list(dict.fromkeys(repositoryLinks))

# save repository links
with open('MLCQUniqueRepos.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(sorted(repositoryLinks))

# check which repositories use github issue tracker
githubRepositories = []

for rowId in range(0, len(repositoryLinks)):
    if get(repositoryLinks[rowId] + "/issues"):
        githubRepositories.append(repositoryLinks[rowId])

# save github issue tracker repositories
with open('MLCQGithubRepos.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(sorted(githubRepositories))

# remove github repositories from the rest of the repositories
nonGithubRepositories = list(set(repositoryLinks) - set(githubRepositories))

# save repos
with open('MLCQDifferentlyIssueTrackedRepos.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(sorted(nonGithubRepositories))
