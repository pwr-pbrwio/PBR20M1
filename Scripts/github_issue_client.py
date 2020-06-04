import requests
import json
import os

token = r'INSERT_GITHUB_TOKEN_HERE'
headers = {'Authorization': 'token {}'.format(token)}

REPO_NAME = 'mockito'
REPO_OWNER = 'mockito'

FIRST_PAGE_ISSUES_QUERY = """
query ($REPO_OWNER: String!, $REPO_NAME: String!) {
  repository (owner: $REPO_OWNER, name: $REPO_NAME) {
    issues (states: [CLOSED], labels: ["bug"], first: 100) {
		nodes {
            number
            createdAt
            closedAt
            }
        pageInfo {
            endCursor
        }
        }
    }
}"""

ISSUES_QUERY_TEMPLATE = """
query ($REPO_OWNER: String!, $REPO_NAME: String!, $END_CURSOR: String!) {
  repository (owner: $REPO_OWNER, name: $REPO_NAME) {
    issues (states: [CLOSED], labels: ["bug"], first: 100, after: $END_CURSOR) {
		nodes {
            number
            createdAt
            closedAt
            }
        pageInfo {
            endCursor
        }
        }
    }
}"""

GITHUB_API_ENDPOINT = 'https://api.github.com/graphql'


def fetchAllIssues(repoOwner, repoName):
    allIssues = []
    issuesPage = fetchIssuesPage(repoOwner, repoName)
    while len(issuesPage['nodes']) > 0:
        cursor = issuesPage['pageInfo']['endCursor']
        allIssues += issuesPage['nodes']
        issuesPage = fetchIssuesPage(repoOwner, repoName, cursor=cursor)

    return allIssues


def fetchIssuesPage(repoOwner, repoName, cursor=None):
    query = getRequestBody(cursor=cursor)
    variables = {
        'REPO_OWNER': repoOwner,
        'REPO_NAME': repoName,
        'END_CURSOR': cursor
    }
    body = {
        'query': query,
        'variables': variables
    }
    r = requests.post(url=GITHUB_API_ENDPOINT,
                      headers=headers, json=body)
    return r.json()['data']['repository']['issues']


def getRequestBody(cursor):
    if cursor == None:
        return FIRST_PAGE_ISSUES_QUERY
    return ISSUES_QUERY_TEMPLATE


def fetch(repoOwner, repoName, outputPath):
    print(repoOwner, repoName, outputPath)
    issuesList = []
    for issue in fetchAllIssues(repoOwner, repoName):
        issuesList.append({
            'key': str(issue['number']),
            'fields': {
                'created': issue['createdAt'],
                'resolutiondate': issue['closedAt']
            }
        })

    issues = {
        'issues': issuesList
    }
    os.makedirs(outputPath + '/', exist_ok=True)
    with open(outputPath + '/res0.json', 'w') as outfile:
        json.dump(issues, outfile)
