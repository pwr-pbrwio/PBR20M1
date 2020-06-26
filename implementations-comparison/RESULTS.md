# Analysis

Results of the `commons-bcel` were used.

## OpenSZZ

- 250 results in 3m30s
- Results contain commits that do not have common files changes. Example:
  - ```
    {
        "bugFixingId": "4d89da4f52f6ae26a4917ba79259e8c89c67eb77",
        "bugFixingTs": "4/12/2019 15:05",
        "bugFixingfileChanged": "src/main/java/org/apache/bcel/classfile/Attribute.java",
        "bugInducingId": "45da20f49abafa125ff4f616e8312b89fbd1f139",
        "bugInducingTs": "2/11/2019 16:26",
        "issueType": "Bug"
        }
    ```

## UnleashedSZZ

- 700 results in 6m
- A lot of the results is fake due to taking greatly into accounts files like changes.xml.
  A signle commit changing only a line in this file is fixing 80 bugs and inducing 120.
- Outputs duplicates of results without any extra data. In this case OpenSZZ also adds a file that in which the changes occured.
- Does not take refactoring into account

## Both

- Most of the results are worthless due to "Major" releases or refactoring changes.
- Matching pairs count: 27
- Matching unique pairs count: 11

## Summary

Many resulting pairs were compared manually based on both the changed logic and changed files.
Most of those cases resulted in exclusion of some of the commits in further analysis due to formatting changes or release commits.
Hardly any real bug introducing and bug fixing pairs were found for both of the implementations.

## Script output

```text
##### Comparison results #####
Matching pairs count: 27
Matching unique pairs count: 11


##### openszz #####
Results count: 249
Results count without fake inducing commits: 24
Results count without fake fixing commits: 249
Results count without fake commits: 24
Results count without fake commits and duplicates: 15


##### unleashedszz #####
Results count: 708
Results count without fake inducing commits: 458
Results count without fake fixing commits: 468
Results count without fake commits: 220
Results count without fake commits and duplicates: 86
```
