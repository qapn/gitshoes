import click
import logging
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
    print('user: %s' % user)
    print('repo: %s' % repo)
    print('token: %s' % token)
    print('filename: %s' % filename)

    github = Github(token)
    repo = github.get_repo(user + "/" + repo)
    repo.get_issues(state='open')
    issues = repo.get_issues(state='open')

    print(issues[10])


# Entrypoint for running the main loop
if __name__ == '__main__':
    run()
