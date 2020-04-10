import csv


def display(filename):
    data = []
    with open(filename, 'r', newline='') as csvFile:
        reader = csv.reader(csvFile, delimiter=',', quotechar='|')
        readerlist = list(reader)

        for rowId in range(0, len(readerlist)):
            for cellId in range(0, len(readerlist[rowId])):
                data.append(readerlist[rowId][cellId])

    print("Count: ")
    print(len(data))
    print("List: ")
    for rowId in range(0, len(data)):
        print(data[rowId])


print("Github repositories")
display("MLCQGithubRepos.csv")

print("Different repositories")
display("MLCQDifferentlyIssueTrackedRepos.csv")
