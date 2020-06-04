import os
import argparse
import json
import csv

from unleashed.fetch import fetch
from unleashed.git_log_to_array import git_log_to_json
from unleashed.find_bug_fixes import find_bug_fixes

from pbr.getFirstSha import getFirstSha

csvPath = os.path.dirname(__file__) + '/git_neto.csv'

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="""Convert a git log output to json.""")
    parser.add_argument('--repoPath', type=str,
                        help="A path to repo.")
    parser.add_argument('--jira', type=str,
                        help="Jira url.")
    parser.add_argument('--owner', type=str,
                        help="Owner of repo.")
    parser.add_argument('--repo', type=str,
                        help="Repo name.")
    parser.add_argument('--tag', type=str,
                        help="Jira tag.")

    data = []
    with open(csvPath, newline='', encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        readerList = list(reader)

        labels = None
        for rowId in range(1):
            labels = readerList[rowId]
        for rowId in range(1, len(readerList)):
            z = zip(labels, readerList[rowId])
            data.append(dict(z))
    data = list(map(lambda x: x['bugfix_commit'], data))

    try:
        args = parser.parse_args()
        repoPath = args.repoPath
        jira = args.jira
        repo = args.repo
        owner = args.owner
        tag = args.tag

        os.makedirs('.temp', exist_ok=True)
        fetch(tag, jira, '.temp/fetch_issues')

        sha = getFirstSha(owner, repo)
        git_log_to_json(sha, repoPath, '.temp')
        issue_list = find_bug_fixes('.temp/fetch_issues', '.temp/gitlog.json',
                                    r'{tag}-{{nbr}}\D|#{{nbr}}\D'.format(tag=tag.upper()))

        toSave = {}

        for key, issue in issue_list.items():
            if issue['hash'] in data:
                toSave[key] = issue

        issue_list = toSave

        with open('.temp/issue_list.json', 'w', encoding="utf8") as f:
            f.write(json.dumps(issue_list))

    except Exception as e:
        print('\u001b[31m{} failed with {}!!!\u001b[0m'.format(repo, e))
