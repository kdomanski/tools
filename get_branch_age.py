#!/usr/bin/env python3

from github import Github
from datetime import datetime
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

branches = []

print("Fetching branch info")
for branch in repo.get_branches():
    branches.append((branch.name, branch.commit.commit.author.date))
print("done")

branches.sort(key=lambda x: x[1])

now = datetime.now()

for branch in branches:
    print("%s %s" % (branch[0], now-branch[1]))