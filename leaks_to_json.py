import git
import re
import pandas as pd
import sys
import signal

def handler_signal(signal, frame):
    print('\n\n [!] Out......... \n')
    sys.exit(1)
signal.signal(signal.SIGINT,handler_signal)

def extract():
    repo = git.Repo('skale/skale-manager')
    with open('commits.txt', 'w') as f:
        for commit in repo.iter_commits():
            f.write(str(commit.message) + '\n')

def git_leaks():
    keywords = ['password', 'secret', 'key', 'token', 'credential', 'access', 'private', 'secret', 'leak']
    leaks = {}
    i = 1
    with open('commits.txt', 'r') as f:
        for line in f:
            for keyword in keywords:
                if re.search(keyword, line, re.IGNORECASE):
                    leaks[i] = line
                    i += 1
                    break
    df = pd.DataFrame(leaks.items(), columns=['leak', 'commit'])

    df.to_json('./data/leaks.json', orient='records')


    
if __name__ == '__main__':
    extract()
    git_leaks()

