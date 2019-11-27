#!/usr/bin/env python3

import github

import argparse
import os
import sys

if not 'GITHUB_TOKEN' in os.environ.keys():
    print("you must provide a Github token in the GITHUB_TOKEN environmental variable")
    exit(1)
g = github.Github(os.environ['GITHUB_TOKEN'])

parser = argparse.ArgumentParser()
parser.add_argument("-r", "--repos", help="repos to check", nargs='+')
parser.add_argument("-l", "--labels", help="labels to check", nargs='+')
args = parser.parse_args()

if args.repos == None:
    print("you must provide a list of repositories to check")
    exit(1)

if args.labels == None:
    print("you must provide a list of labels to check for")
    exit(1)

def hasAnyOfTheLabels(issue: github.Issue.Issue, expected_labels: [str]):
    for label in issue.labels:
        if label.name in expected_labels:
            return True
    return False

for reposlug in args.repos:
    unlabelled_issues = []
    for issue in g.get_repo(reposlug).get_issues():
        if issue.state == 'open' and not hasAnyOfTheLabels(issue, args.labels):
            unlabelled_issues.append(issue)
    if len(unlabelled_issues) > 0:
        print("Repo %s:" % reposlug)
        for i in unlabelled_issues:
            print("\thttps://github.com/%s/issues/%d %s" % (reposlug, i.number, i.title))
        print("")
