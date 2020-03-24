import os
from getMLCQRepositories import getMLCQRepos

mlcqCSVPath = r'MLCQCodeSmellSamples.csv'
commandFormat = r'git clone https://github.com/{owner}/{repo}.git repos/{owner}/{repo}'

def cloneRepo(owner, repo):
  os.system(commandFormat.format(owner=owner, repo=repo))

def main():
  repos = getMLCQRepos(mlcqCSVPath)
  flist = filter(lambda x: x[0] == 'apache', repos)
  apacheRepos = list(flist)
  for repo in apacheRepos:
    cloneRepo(repo[0], repo[1])


if __name__ == "__main__":
  main()
