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
        writer.writerow(['Number', 'Created At', 'Updated At', 'Title', 'Description', 'Labels', 'Assignees'])
        for issue in issues:
            writer.writerow([issue.number, issue.created_at, issue.updated_at, issue.title, issue.body, get_nested_items(issue.labels, 'labels'), get_nested_items(issue.assignees, 'assignees')])
    write_report.close()

    print(str(issues.totalCount) + ' issues written to ' + filename)

# Return a concatenated string from nested items, takes a list of either labels or assignees from an issue as input
def get_nested_items(nested_items, type):
    concat_string = ''
    for x, item in enumerate(nested_items, 1):
        if type == 'labels':
            concat_string += item.name
        elif type == 'assignees':
            concat_string += item.login
        if x != len(nested_items):
            concat_string += ', '
    return concat_string

# Entrypoint for running the main loop
if __name__ == '__main__':
    run()
