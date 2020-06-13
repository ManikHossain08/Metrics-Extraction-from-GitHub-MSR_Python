# Metrics-Extraction-from-GitHub-MSR
The main task of the tool is extract metrics (e.g., #commits, #tags, #authors etc from the projects) from GitHub projects according to the settings that are related to the people i.e. the number of the developer in the project, the number of commits per project, the number of commits per developer in a project and so on using Python

# Steps to run the tool
open acanoda/PyCharm editor

move source code to the specific location and change the config file according to your directory.

Run following command on your terminal: 

- 1. First to Download the source code to the local machine for further analysis: 
$ python aliasloginjoiner.py 5d6522e3fa8c4fd03f7f70d8ac3c10e09bf7aebf


- 2. Second Find the indicated metrics from downloaded GitHub source code: 
$ python main.py 
