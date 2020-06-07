import requests
import json
import os
import datetime

token = r'INSERT_GITHUB_TOKEN_HERE'
headers = {'Authorization': 'token {}'.format(token)}


FIRST_PAGE_ISSUES_QUERY = """
query ($REPO_OWNER: String!, $REPO_NAME: String!, $BUG_LABEL: String!) {
  repository (owner: $REPO_OWNER, name: $REPO_NAME) {
    issues (states: [CLOSED], labels: [$BUG_LABEL], first: 100) {
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
query ($REPO_OWNER: String!, $REPO_NAME: String!, $END_CURSOR: String!, $BUG_LABEL: String!) {
  repository (owner: $REPO_OWNER, name: $REPO_NAME) {
    issues (states: [CLOSED], labels: [$BUG_LABEL], first: 100, after: $END_CURSOR) {
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


def fetchAllIssues(repoOwner, repoName, bugLabelName):
    allIssues = []
    issuesPage = fetchIssuesPage(repoOwner, repoName, bugLabelName)
    while len(issuesPage['nodes']) > 0:
        cursor = issuesPage['pageInfo']['endCursor']
        allIssues += issuesPage['nodes']
        issuesPage = fetchIssuesPage(
            repoOwner, repoName, bugLabelName, cursor=cursor)

    return allIssues


def fetchIssuesPage(repoOwner, repoName, bugLabelName, cursor=None):
    query = getRequestBody(cursor=cursor)
    variables = {
        'REPO_OWNER': repoOwner,
        'REPO_NAME': repoName,
        'END_CURSOR': cursor,
        'BUG_LABEL': bugLabelName
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


def formatDate(date):
    date = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S%z")
    return date.strftime("%Y-%m-%d %H:%M:%S %z")


def fetch(repoOwner, repoName, outputPath, bugLabelName):
    issuesList = []
    for issue in fetchAllIssues(repoOwner, repoName, bugLabelName):
        issuesList.append({
            'key': str(issue['number']),
            'fields': {
                'created': formatDate(issue['createdAt']),
                'resolutiondate': formatDate(issue['closedAt'])
            }
        })

    issues = {
        'issues': issuesList
    }
    os.makedirs(outputPath + '/', exist_ok=True)
    with open(outputPath + '/res0.json', 'w') as outfile:
        json.dump(issues, outfile)
