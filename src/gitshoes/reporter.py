import click
import logging
import csv
import sys
from github import Github
from github import GithubException

from gitshoes import __version__

@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.version_option()
@click.option('-u', '--user', help='GitHub username or organisation name.', required=True)
@click.option('-r', '--repository', help='GitHub repository name.', required=True)
@click.option('-t', '--token', help='GitHub OAuth token.', required=True)
@click.option('-f', '--filename', default='issues.csv', help='Output (CSV) filename.')

# Main application loop
def run(user, repository, token, filename):
    github = Github(token)
    try:
        repo = github.get_repo(user + '/' + repository)
    except GithubException as e:
        repo = None
        print("GitHub returned the following error: '" + e.data.get('message') + "'. Check your username/repository/token and try again.")
        sys.exit(1)

    issues = repo.get_issues(state='open')

    print('Retrieving ' + str(issues.totalCount) + ' issues from ' + user + '/' + repository + '...')

    with open(filename, 'w') as write_report:
        writer = csv.writer(write_report)
        writer.writerow(['Number', 'Created At', 'Updated At', 'Title', 'Description', 'Labels'])
        for issue in issues:
            writer.writerow([issue.number, issue.created_at, issue.updated_at, issue.title, issue.body, get_labels(issue.labels)])
    write_report.close()

    print(str(issues.totalCount) + ' issues written to ' + filename)

# Return a concatenated labels string, takes a label list from an issue as input
def get_labels(labels):
    labels_string = ""
    for x, label in enumerate(labels, 1):
        labels_string += label.name
        if x != len(labels):
            labels_string += ", "
    return labels_string

# Entrypoint for running the main loop
if __name__ == '__main__':
    run()
