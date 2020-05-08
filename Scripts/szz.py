import os
import argparse
import json

from unleashed.fetch import fetch
from unleashed.git_log_to_array import git_log_to_json
from unleashed.find_bug_fixes import find_bug_fixes

from pbr.getFirstSha import getFirstSha

commandFormat = r'java -jar "{file}/unleashed/szz.jar" -i ".temp/issue_list.json" -r "{repoPath}" -d={depth}'

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
    parser.add_argument('--depth', type=str,
                        help="Szz depth.")

    try:
        args = parser.parse_args()
        repoPath = args.repoPath
        jira = args.jira
        repo = args.repo
        owner = args.owner
        tag = args.tag
        depth = 3 if args.depth == None else args.depth

        os.makedirs('.temp', exist_ok=True)
        fetch(tag, jira, '.temp/fetch_issues')

        sha = getFirstSha(owner, repo)
        git_log_to_json(sha, repoPath, '.temp')
        issue_list = find_bug_fixes('.temp/fetch_issues', '.temp/gitlog.json',
                                    r'{tag}-{{nbr}}\D|#{{nbr}}\D'.format(tag=tag.upper()))

        with open('.temp/issue_list.json', 'w', encoding="utf8") as f:
            f.write(json.dumps(issue_list))

        print('Run unleashed szz...')
        os.system(commandFormat.format(file=os.path.dirname(
            os.path.realpath(__file__)), repoPath=repoPath, depth=depth))

    except Exception as e:
        print('\u001b[31m{} failed with {}!!!\u001b[0m'.format(repo, e))
