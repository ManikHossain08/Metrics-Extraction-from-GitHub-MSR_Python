import os
import git
import csv
from datetime import datetime

from progress.bar import Bar

def tagAnalysis(repo: git.Repo, outputDir: str):
    print("Analyzing tags")

    tagInfo = []
    tags = sorted(repo.tags, key=getTaggedDate)
    
    lastTag = None
    for tag in Bar('Processing').iter(tags):
        commitCount = 0
        if (lastTag == None):
            commitCount = len(list(tag.commit.iter_items(repo, tag.commit)))
        else:
            sinceStr = formatDate(getTaggedDate(lastTag))
            commitCount = len(list(tag.commit.iter_items(repo, tag.commit, after=sinceStr)))
        
        tagInfo.append(dict(
            path=tag.path,
            date= formatDate(getTaggedDate(tag)),
            commitCount= commitCount
        ))
        
        lastTag = tag

    # output non-tabular results
    with open(os.path.join(outputDir, 'project.csv'), 'a', newline='') as f:
        w = csv.writer(f, delimiter=',')
        w.writerow(['Tag Count', len(tagInfo)])

    # output tag info
    print("Outputting CSVs")
    with open(os.path.join(outputDir, 'tags.csv'), 'a', newline='') as f:
        w = csv.writer(f, delimiter=',')
        w.writerow(['Path', 'Date', 'Commit Count'])
        for tag in sorted(tagInfo, key=lambda o: o['date']):
            w.writerow([tag['path'], tag['date'], tag['commitCount']])

def getTaggedDate(tag):
    date = None
    
    if tag.tag == None:
        date = tag.commit.committed_date
    else:
        date = tag.tag.tagged_date
        
    date = datetime.fromtimestamp(date)
    return date

def formatDate(value):
    return value.strftime('%Y-%m-%d')