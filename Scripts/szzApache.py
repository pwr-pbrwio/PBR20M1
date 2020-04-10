import multiprocessing as mp
import os.path
import os

from pbr.getMLCQRepositories import getMLCQRepos


# Before running this script first download all repositories

# Path to MLCQ database in cvs format
mlcqCSVPath = r'MLCQCodeSmellSamples.csv'
commandFormat = r'java -jar ../../../../unleashed/szz_find_bug_introducers.jar -i "./issue_list.json" -r "../../../repos/{owner}/{repo}"'

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
      print('{} szz started...'.format(repo))
      os.chdir(r'.temp/szz/{owner}/{repo}'.format(owner=owner, repo=repo))
      os.system(commandFormat.format(owner=owner, repo=repo))
      os.chdir(r'../../../..')
      
      print('{} done.'.format(repo))
    except:
      print('\u001b[31m{} failed!!!\u001b[0m'.format(repo))

repos = getMLCQRepos(mlcqCSVPath)
flist = sorted(filter(lambda x: x[0] == 'apache', repos))


chunks = chunkIt(flist, 1)
for chunk in chunks:
  process(chunk)