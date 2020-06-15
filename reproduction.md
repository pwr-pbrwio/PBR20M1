# Research reproduction

## Dependencies
+ git
+ java 8
+ python 3

## Dependencies installation (windows and macos)
Download and install dependencies:
+ git: https://git-scm.com/
+ java: https://www.oracle.com/java/technologies/javase-jre8-downloads.html
+ python: https://www.python.org/

## Dependencies installation(linux)
```
sudo apt update
sudo apt install git
sudo apt-get install openjdk-8-jre
sudo apt-get install python3
```

## Steps to reproduce
On windows replace python3 with python and pip3 with pip

Prepare szz
```
git clone https://github.com/pwr-pbrwio/PBR20M1
cd PBR20M1
pip3 install -r requirements.txt
```
Get repository from data set (example of commons-lang)
```
mkdir commons-lang
cd commons-lang
git clone https://github.com/apache/commons-lang.git
```
Download project issues (filtered with data set)
If using Jira as issue tracker
```
python3 ../PBR20M1/Scripts/getNetoIssuesJira.py --owner "apache" --repo "commons-lang" --tag "lang" --repoPath "./commons-lang" --jira "issues.apache.org/jira"
```
If using Github as issue tracker (mockito as example)
```
python3 ..\PBR20M1\Scripts\getNetoIssuesJira.py --owner "mockito" --repo "mockito" --repoPath "./mockito" --fetchStrategy github
```
Run szz algorithm
```
java -jar "../PBR20M1/Scripts/unleashed/szz.jar" -i ".temp/issue_list.json" -r "./commons-lang" -d=3  -fix -ra -up -mt -fp
```
Where flags -fix -ra -up -mt -fp are optional
-fix enables fix
-ra runs SZZ with refactoring awareness
-up removes comments
-mt limits time between commits to 2 years
-fp limits SZZ to .java files

Get results
```
python3 ../PBR20M1/Scripts/measurePos.py --repoName="commons-lang"
```
Or for OpenSZZ
```
python3 ../PBR20M1/Scripts/openSzzAcc.py --repoName="commons-lang"
```
