import requests

githubRepoUrl = r'https://api.github.com/repos/{owner}/{repo}'
githubCommitsUrl = r'https://api.github.com/repos/{owner}/{repo}/commits?per_page=100&page={page}&until={until}'

def getCreationDate(owner, repo):
  r = requests.get(url = githubRepoUrl.format(owner=owner, repo=repo))
  return r.json()['created_at']

def getFirstSha(owner, repo):
  l = []
  while(True):
    # r = requests.get(url = githubCommitsUrl.format(owner=owner, repo=repo, page=1))
    # data = r.json()
    # if len(data) == 0:
    #   break
    # l = data
    break
  
  if len(l) == 0:
    raise ValueError('Failed to fetch first commit of {}'.format(repo))

  first = (l[0].sha, l[0].commit.date)
  for i in range(1, len(l)):
    if l[i].commit.date < first[1]:
      first = (l[i].sha, l[i].commit.date)

  return first[0]

getCreationDate('apache', 'syncope')
