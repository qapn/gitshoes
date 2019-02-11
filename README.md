# Gitshoes

Generates a CSV report on issues in a GitHub repository. Gitshoes is written in Python 3 and uses [Click](https://github.com/pallets/click) to build a command line interface, and [PyGitHub](https://github.com/PyGithub/PyGithub) to interact with the GitHub API.

## Install

```
pip install gitshoes
```

## Options
```
Usage: gitshoes [OPTIONS]

Options:
  --version              Show the version and exit.
  -u, --user TEXT        GitHub username or organisation name.  [required]
  -r, --repository TEXT  GitHub repository name.  [required]
  -t, --token TEXT       GitHub OAuth token.  [required]
  -f, --filename TEXT    Output (CSV) filename.
  -d, --date TEXT        Retrieve only issues since the provided date (format:
                         YYYY/MM/DD).
  -c, --closed           Retrieve closed issues instead of open issues.
  -h, --help             Show this message and exit.
```

## Usage

To generate a list of open issues:
```
gitshoes -u <USERNAME> -r <REPOSITORY> -t <TOKEN>
```

To generate a list of closed issues since 1st of January 2019, including the tag the issue was closed in (useful for changelogs):
```
gitshoes -u <USERNAME> -r <REPOSITORY> -t <TOKEN> -d "2019/01/01" -c
```
