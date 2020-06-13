import os
import git
import yaml

from progress.bar import Bar

def replaceAliases(repo: git.Repo, aliasPath: str):
    print("Cleaning aliased authors")
    
    # quick lowercase and trim if no alias file
    if aliasPath == None or not os.path.exists(aliasPath):
        return replaceAll(repo.iter_commits(), {})
    
    # read aliases
    content = ""
    with open(aliasPath, 'r', encoding='utf-8-sig') as file:
        content = file.read()
        
    aliases = yaml.load(content)
    
    # transpose for easy replacements
    transposesAliases = {}
    for alias in aliases:
        for email in aliases[alias]:
            transposesAliases[email] = alias
            
    # replace all author aliases with a unique one
    return replaceAll(repo.iter_commits(), transposesAliases)

def replaceAll(commits, aliases):
    for commit in Bar('Processing').iter(list(commits)):
        copy = commit
        author = commit.author.email.lower().strip()
        
        if author in aliases:
            copy.author.email = aliases[author]
            yield copy
        else:
            copy.author.email = author
            yield commit