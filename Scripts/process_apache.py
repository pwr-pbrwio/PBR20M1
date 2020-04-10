from unleashed.fetch import fetch
from unleashed.git_log_to_array import git_log_to_json
from unleashed.find_bug_fixes import find_bug_fixes
import json

import multiprocessing as mp
import os.path

from pbr.getMLCQRepositories import getMLCQRepos
from pbr.getFirstSha import getFirstSha


# First download all repositories

# Path to MLCQ database in cvs format
mlcqCSVPath = r'MLCQCodeSmellSamples.csv'

def chunkIt(seq, num):
  avg = len(seq) / float(num)
  out = []
  last = 0.0
  l = len(seq)

  while last < l:
    out.append(seq[int(last):int(last + avg)])
    last += avg

  return out

def process(li):
  for x in li:
    try:
      owner = x[0]
      repo = x[1]
      print('{} starting...'.format(repo))

      # fetch('{}'.format(repo), 'issues.apache.org/jira', '.temp/szz/{}/{}/fetch_issues'.format(owner, repo))
      sha = getFirstSha(owner, repo)
      print(sha)
      git_log_to_json(getFirstSha(owner, repo), '.temp/repos/{}/{}'.format(owner, repo), '.temp/szz/{}/{}'.format(owner, repo))
      issue_list = find_bug_fixes('.temp/szz/{}/{}/fetch_issues'.format(owner, repo), '.temp/szz/{}/{}/gitlog.json'.format(owner, repo), r'{repo}-{{nbr}}\D|#{{nbr}}\D'.format(repo=repo.upper()))

      with open('.temp/szz/{}/{}/issue_list.json'.format(owner, repo), 'w') as f:
        f.write(json.dumps(issue_list))
      
      print('{} done.'.format(repo))
    except:
      print('\u001b[31m{} failed!!!\u001b[0m'.format(repo))

repos = getMLCQRepos(mlcqCSVPath)
flist = sorted(filter(lambda x: x[0] == 'apache', repos))


ctx = mp.get_context('spawn')

chunks = chunkIt(flist, 8)
for chunk in chunks:
  mp.Process(target=process, args=(chunk, )).start()