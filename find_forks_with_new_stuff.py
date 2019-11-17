#!/usr/bin/env python3

from github import Github
import os
import sys

if not 'GITHUB_TOKEN' in os.environ.keys():
    print("you must provide a Github token in the GITHUB_TOKEN environmental variable")
    exit(1)

if len(sys.argv) < 2:
    print("you must provide a git repo slug in the first argument")
    exit(1)

g = Github(os.environ['GITHUB_TOKEN'])
repo = g.get_repo(sys.argv[1])
original_branches = repo.get_branches()

original_commits = set()

print("Getting commits for original branches:")
for branch in original_branches:
    commits = repo.get_commits(sha=branch.commit.sha)
    for commit in commits:
        original_commits.add(commit.sha)
    print("  " + branch.name )

print("\nThe following forks/branches have tips not contained in the source repo history:")
for fork in repo.get_forks():
    for branch in fork.get_branches():
        if branch.commit.sha not in original_commits:
            print("  %s : %s" % (fork.full_name, branch.name))
            