# %%
import requests

token = r'INSERT_GITHUB_TOKEN_HERE'
githubRepoUrl = r'https://api.github.com/repos/{owner}/{repo}'
# githubCommitsUrl = r'https://api.github.com/repos/{owner}/{repo}/commits?per_page=1&page=1&until={until}'
githubCommitsUrl = r'https://api.github.com/repos/{owner}/{repo}/commits?per_page=1&page=1&until=2020-01-01T00:00:00Z'

headers = {'Authorization': 'token {}'.format(token)}


def getCreationDate(owner, repo):
    try:
        r = requests.get(url=githubRepoUrl.format(
            owner=owner, repo=repo), headers=headers)
        return r.json()['created_at']
    except Exception as e:
        print(e)
        return None


def getFirstSha(owner, repo):
    # until = getCreationDate(owner, repo)
    # if until == None:
    #   raise ValueError('Failed to fetch creation data of {}'.format(repo))
    r = requests.get(url=githubCommitsUrl.format(
        owner=owner, repo=repo), headers=headers)
    data = r.json()
    if data == None or len(data) == 0:
        raise ValueError('Failed to fetch first commit of {}'.format(repo))

    return data[0]['sha']

# %%
