import git
import csv
import os

from typing import List
from collections import Counter
from progress.bar import Bar
from datetime import datetime
    
def commitAnalysis(commits: List[git.Commit], outputDir: str):
    
    authorInfoDict = {}
    timezoneInfoDict = {}
    
    # traverse all commits
    print("Analyzing commits")
    for commit in Bar('Processing').iter(commits):
        
        # extract info
        author = commit.author.email
        timezone = commit.author_tz_offset
        time = commit.authored_datetime
        
        # get timezone
        timezoneInfo = timezoneInfoDict.setdefault(timezone, dict(
                commitCount=0,
                authors=set()
        ))
        
        # save author
        timezoneInfo['authors'].add(author)
        
        # increase commit count
        timezoneInfo['commitCount'] += 1
        
        # get author
        authorInfo = authorInfoDict.setdefault(author, dict(
                commitCount= 0,
                sponsoredCommitCount= 0,
                earliestCommitDate=time,
                latestCommitDate=time
        ))
        
        # increase commit count
        authorInfo['commitCount'] += 1
        
        # validate earliest commit
        # by default GitPython orders commits from latest to earliest
        if (time < authorInfo['earliestCommitDate']):
            authorInfo['earliestCommitDate'] = time
        
        # check if commit was between 9 and 5
        if not commit.author_tz_offset == 0 and time.hour >= 9 and time.hour <= 17:
            authorInfo['sponsoredCommitCount'] += 1
        
    # calculate amount of sponsored devs
    print("Analyzing sponsored authors")
    sponsoredAuthorCount = 0
    for author in authorInfoDict:
        info = authorInfoDict[author]
        commitCount = int(info['commitCount'])
        sponsoredCommitCount = int(info['sponsoredCommitCount'])
        diff = sponsoredCommitCount / commitCount
        if diff >= .95:
            sponsoredAuthorCount += 1
            
    # calculate active project days
    firstCommitDate = datetime.fromtimestamp(commits[len(commits) - 1].committed_date)
    lastCommitDate = datetime.fromtimestamp(commits[0].committed_date)
    daysActive = (lastCommitDate - firstCommitDate).days	
    
    print("Outputting CSVs")
    
    # output author days on project
    with open(os.path.join(outputDir, 'authorDaysOnProject.csv'), 'a', newline='') as f:
        w = csv.writer(f, delimiter=',')
        w.writerow(['Author','# of Days'])
        for author in authorInfoDict:
            earliestDate = authorInfoDict[author]['earliestCommitDate']
            latestDate = authorInfoDict[author]['latestCommitDate']
            diff = latestDate - earliestDate
            w.writerow([author,diff.days + 1])
    
    with open(os.path.join(outputDir, 'timezones.csv'), 'a', newline='') as f:
        w = csv.writer(f, delimiter=',')
        w.writerow(['Timezone Offset','Author Count','Commit Count'])
        for timezone in timezoneInfoDict:
            timezoneInfo = timezoneInfoDict[timezone]
            w.writerow([timezone,len(timezoneInfo['authors']),timezoneInfo['commitCount']])
            
    # output commits per author
    with open(os.path.join(outputDir, 'commitsPerAuthor.csv'), 'a', newline='') as f:
        w = csv.writer(f, delimiter=',')
        w.writerow(['Author','Commit Count'])
        for author in authorInfoDict:
            w.writerow([author,authorInfoDict[author]['commitCount']])
        
    # output project info
    with open(os.path.join(outputDir, 'project.csv'), 'a', newline='') as f:
        w = csv.writer(f, delimiter=',')
        w.writerow(['DaysActive', daysActive])
        w.writerow(['FirstCommitDate', '{:%Y-%m-%d}'.format(firstCommitDate)])
        w.writerow(['LastCommitDate', '{:%Y-%m-%d}'.format(lastCommitDate)])
        w.writerow(['AuthorCount',len([*authorInfoDict])])
        w.writerow(['SponsoredAuthorCount',sponsoredAuthorCount])
        w.writerow(['TimezoneCount',len([*timezoneInfoDict])])