import os
import subprocess
from getMLCQRepositories import getMLCQRepos

mlcqCSVPath = r'MLCQCodeSmellSamples.csv'
commandFormat = r'python ..\..\SZZUnleashed\fetch_jira_bugs\fetch.py --issue-code "{repo}" --jira-project "issues.apache.org/jira"'


def main():
  repos = getMLCQRepos(mlcqCSVPath)
  flist = filter(lambda x: x[0] == 'apache', repos)
  for repo in flist:
    os.mkdir('issues/{}'.format(repo[1]))
    os.chdir('./issues/{repo}'.format(repo=repo[1]))
    os.system(commandFormat.format(repo=repo[1]))
    os.chdir('../..')


if __name__ == "__main__":
  main()

