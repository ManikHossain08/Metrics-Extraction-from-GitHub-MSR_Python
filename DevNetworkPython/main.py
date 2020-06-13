import os
import shutil
import git
import yaml

from configuration import Configuration
from repoLoader import getRepo
from aliasWorker import replaceAliases
from commitAnalysis import commitAnalysis
from centralityAnalysis import centralityAnalysis
from tagAnalysis import tagAnalysis


def main():
    try:
        # read configuration
        config = ...  # type: Configuration
        with open('config.yml', 'r', encoding='utf-8-sig') as file:
            content = file.read()
            config = yaml.load(content)
        
        # get repository reference
        repo = getRepo(config)
            
        # delete any existing output files
        if os.path.exists(config.analysisOutputPath):
            shutil.rmtree(config.analysisOutputPath)
            
        os.makedirs(config.analysisOutputPath)
        
        # handle aliases
        commits = list(replaceAliases(repo, config.aliasPath))
            
        # run analysis
        tagAnalysis(repo, config.analysisOutputPath)
        commitAnalysis(commits, config.analysisOutputPath)
        centralityAnalysis(repo, commits, config.analysisOutputPath)
        
    finally:
        # close repo to avoid resource leaks
        del repo


class Progress(git.remote.RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=''):
        print(self._cur_line, end="\r")


def commitDate(tag):
    return tag.commit.committed_date


main()