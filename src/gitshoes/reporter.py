import click
import logging
import csv
import sys
from datetime import datetime
from github import Github
from github import GithubException

from gitshoes import __version__

@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.version_option()
@click.option('-u', '--user', help='GitHub username or organisation name.', required=True)
@click.option('-r', '--repository', help='GitHub repository name.', required=True)
@click.option('-t', '--token', help='GitHub OAuth token.', required=True)
@click.option('-f', '--filename', default='issues.csv', help='Output (CSV) filename.')
@click.option('-d', '--date', help='Retrieve only issues since the provided date (format: YYYY/MM/DD).')
@click.option('-c', '--closed', is_flag=True, help='Retrieve closed issues instead of open issues.')

# Main application loop
def run(user, repository, token, filename, date, closed):
    github = Github(token)
    try:
        repo = github.get_repo(user + '/' + repository)
    except GithubException as e:
        repo = None
        print("GitHub returned the following error: '" + e.data.get('message') + "'. Check your username/repository/token and try again.")
        sys.exit(1)

    if closed:
        state = 'closed'
    else:
        state = 'open'

    if date:
        try:
            date = datetime.strptime(date, '%Y/%m/%d')
        except ValueError:
            print("Invalid date format provided, please make sure you're entering the date in the format 'YYYY/MM/DD'.")
            sys.exit(1)
        issues = repo.get_issues(state=state, since=date)
    else:
        issues = repo.get_issues(state=state)

    print('Retrieving ' + str(issues.totalCount) + ' issues from ' + user + '/' + repository + '...')

    if closed:
        tags = repo.get_tags()
        sorted_tags = list()
        for tag in tags:
            sorted_tags.append((tag.name, datetime.strptime(tag.commit.stats.last_modified, '%a, %d %b %Y %H:%M:%S %Z')))
        sorted_tags.sort(key=lambda x: x[1])

    with open(filename, 'w') as write_report:
        writer = csv.writer(write_report)
        if closed:
            writer.writerow(['Number', 'Created At', 'Updated At', 'Closed At', 'Title', 'Description', 'Labels', 'Tag', 'Assignees'])
        else:
            writer.writerow(['Number', 'Created At', 'Updated At', 'Title', 'Description', 'Labels', 'Assignees'])
        for issue in issues:
            if closed:
                writer.writerow([issue.number, issue.created_at, issue.updated_at, issue.closed_at, issue.title, issue.body, get_nested_items(issue.labels, 'labels'), get_issue_tag(issue, sorted_tags), get_nested_items(issue.assignees, 'assignees')])
            else:
                writer.writerow([issue.number, issue.created_at, issue.updated_at, issue.title, issue.body, get_nested_items(issue.labels, 'labels'), get_nested_items(issue.assignees, 'assignees')])
    write_report.close()

    print(str(issues.totalCount) + ' issues written to ' + filename)

# Return a concatenated string from nested items, takes a list of either labels or assignees from an issue as input
def get_nested_items(nested_items, type):
    concat_string = ''
    for i, item in enumerate(nested_items, 1):
        if type == 'labels':
            concat_string += item.name
        elif type == 'assignees':
            concat_string += item.login
        if i != len(nested_items):
            concat_string += ', '
    return concat_string

# Return the name of the latest tag associated with a closed issue
def get_issue_tag(issue, tags):
    for i, tag in enumerate(tags):
        if tag[1] > issue.closed_at:
            return tag[0]
        elif i+1 == len(tags):
            return 'None'

# Entrypoint for running the main loop
if __name__ == '__main__':
    run()
