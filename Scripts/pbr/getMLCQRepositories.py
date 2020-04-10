# %%
import csv
import re

repoPattern = r'https\:\/\/github\.com\/(?P<owner>[a-z]+)\/(?P<repo>[a-z]+)\/.*'
repoRegex = re.compile(repoPattern)

def getMLCQRepos(csvPath):
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

  repos = set()
  for i in range(len(data)):
    m = repoRegex.match(data[i]['link'])
    if m != None:
      owner = m.group('owner')
      repo = m.group('repo')
      repos.add((owner, repo))
  
  return list(repos)