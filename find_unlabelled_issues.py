#!/usr/bin/env python3

import github

import argparse
import json
import os
import requests
import sys

if not 'GITHUB_TOKEN' in os.environ.keys():
    print("you must provide a Github token in the GITHUB_TOKEN environmental variable")
    exit(1)
g = github.Github(os.environ['GITHUB_TOKEN'])

parser = argparse.ArgumentParser()
parser.add_argument("-r", "--repos", help="repos to check", nargs='+')
parser.add_argument("-l", "--labels", help="labels to check", nargs='+')
parser.add_argument("-w", "--slack_webhook")
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

output = ''

for reposlug in args.repos:
    unlabelled_issues = []
    for issue in g.get_repo(reposlug).get_issues(state='open'):
        if not hasAnyOfTheLabels(issue, args.labels):
            unlabelled_issues.append(issue)
    if len(unlabelled_issues) > 0:
        output += "Repo %s:\n" % reposlug
        for i in unlabelled_issues:
            output += "\thttps://github.com/%s/issues/%d %s\n" % (reposlug, i.number, i.title)
        output += '\n'

if args.slack_webhook == None:
    print(output)
else:
    output = ("The following issues are missing %s labels:\n\n" % args.labels) + output
    payload = json.dumps({'channel': '@kamil', 'text': output})
    r = requests.post(url = args.slack_webhook, data = payload)
    print(r)
