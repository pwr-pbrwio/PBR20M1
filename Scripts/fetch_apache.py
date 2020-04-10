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

def fetchRepos(li):
  for x in li:
    try:
      owner = x[0]
      repo = x[1]
      print('{} fetching...'.format(repo))
      path = '.temp/szz/{}/{}/fetch_issues'.format(owner, repo)
      if os.path.isdir(path):
        print('{} exists, skipping.'.format(repo))
      else:
        fetch('{}'.format(repo), 'issues.apache.org/jira', path)
        print('{} fetched.'.format(repo))
    except OSError:
      print('\u001b[31m{} error fetching!\u001b[0m'.format(repo))
      os.rmdir('.temp/szz/{}/{}/fetch_issues'.format(owner, repo))
      os.rmdir('.temp/szz/{}/{}'.format(owner, repo))

      
    

repos = getMLCQRepos(mlcqCSVPath)
flist = sorted(filter(lambda x: x[0] == 'apache', repos))


ctx = mp.get_context('spawn')

p = []
chunks = chunkIt(flist, 2)
for chunk in chunks:
  pi = mp.Process(target=fetchRepos, args=(chunk, ))
  pi.start()
  p.append(pi)

for pi in p:
  pi.join()