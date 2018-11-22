import click
import logging
import csv
from github import Github

from gitshoes import __version__

@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.version_option()
@click.option('-u', '--user', help='GitHub username or organisation name.', required=True)
@click.option('-r', '--repo', help='GitHub repository name.', required=True)
@click.option('-t', '--token', help='GitHub oAuth token.', required=True)
@click.option('-f', '--filename', default='issues.csv', help='Output (CSV) filename.')

# Main application loop
def run(user, repo, token, filename):
    github = Github(token)
    repo = github.get_repo(user + "/" + repo)
    issues = repo.get_issues(state='open')

    with open(filename, 'w') as write_report:
        writer = csv.writer(write_report)
        writer.writerow(['Number', 'Created At', 'Updated At', 'Title', 'Description', 'Labels'])
        for issue in issues:
            writer.writerow([issue.number, issue.created_at, issue.updated_at, issue.title, issue.body, get_labels(issue.labels)])
    write_report.close()

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
