# Research reproduction

## Dependencies

+ git
+ java 8
+ python 3

## Dependencies installation (windows and macos)

Download and install dependencies:

+ git: <https://git-scm.com/>
+ java: <https://www.oracle.com/java/technologies/javase-jre8-downloads.html>
+ python: <https://www.python.org/>

## Dependencies installation(linux)

```bash
sudo apt update
sudo apt install git
sudo apt-get install openjdk-8-jre
sudo apt-get install python3
```

## Steps to reproduce

### Requirements

+ You will need a [GitHub personal access token](https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token). Place it in `Scripts/token.txt`. It is used for projects using GitHub as issue tracker.

### SZZUnleashed with and without improvements

On windows replace python3 with python and pip3 with pip

1. Prepare szz:

    ```bash
    git clone https://github.com/pwr-pbrwio/PBR20M1
    cd PBR20M1
    pip3 install -r requirements.txt
    cd ..
    ```

2. Get repository from data set (example of commons-lang):

    ```bash
    mkdir commons-lang
    cd commons-lang
    git clone https://github.com/apache/commons-lang.git
    ```

3. Download project issues (filtered with data set)
    If You are using Jira as the issue tracker:

    ```bash
    python3 ../PBR20M1/Scripts/getNetoIssues.py --owner "apache" --repo "commons-lang" --tag "lang" --repoPath "./commons-lang" --jira "issues.apache.org/jira"
    ```

    If You are using GitHub as the issue tracker (e.g. for `mockito`):

    ```bash
    python3 ../PBR20M1/Scripts/getNetoIssues.py --owner "mockito" --repo "mockito" --repoPath "./mockito" --fetchStrategy github
    ```

4. Run the SZZ algorithm:

    ```bash
    java -jar "../PBR20M1/Scripts/unleashed/szz.jar" -i ".temp/issue_list.json" -r "./commons-lang" -d=3  -fix -ra -up -mt -fp
    ```

    Where flags -fix -ra -up -mt -fp are optional:
    -fix enables fix
    -ra runs SZZ with refactoring awareness
    -up removes comments
    -mt limits time between commits to 2 years
    -fp limits SZZ to .java files

5. Get results:

    ```bash
    python3 ../PBR20M1/Scripts/measurePos.py --repoName="commons-lang"
    ```

### OpenSZZ

#### Dependency requirements

The following software is required:

+ docker
+ docker-compose

#### Usage

1. Clone the [OpenSZZ repo](https://github.com/clowee/OpenSZZ-Cloud-Native).
2. Publication was prepared on version `533b4911710753e76c78c02c02ca10707a74e05b`. Make sure the correct version is used.
3. Increase the heap size by adding the `JVM_OPTS` environmental variable to the `web` service in the `docker-compose.yml` file. Note that using docker on windows or linux might require increasing the total memory assigned to docker in the docker settings. Example:

    ```yaml
        web:
            build: ./core
            ports:
            - "${PORTRANGE_FROM}-${PORTRANGE_TO}:8080"
            networks:
            - spring-cloud-network
            depends_on:
            - rabbitmq
            volumes:
            - /var/run/docker.sock:/var/run/docker.sock
            environment:
            - JVM_OPTS=-Xmx12g -Xms12g -XX:MaxPermSize=1024m
    ```

4. Follow the [OpenSZZ readme file](https://github.com/clowee/OpenSZZ-Cloud-Native) for instructions on starting the application and running repositories.
5. Rename results to BugInducingCommits.csv
6. Analyse results

    ```bash
    python3 ../PBR20M1/Scripts/openSzzAcc.py --repoName="commons-lang"
    ```
