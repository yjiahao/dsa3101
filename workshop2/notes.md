# Seminar 2

## Introduction to Git

## Mental model and workflow of Git

1. Current commit always points to the parent commit
2. Head reference -> master reference -> committed file (could be a new version)
    - The new file that is commited points to the parent file: v1 <- v2 <- master <- head
3. We will only have 1 head reference for the entire repository

## Git Branching

## Version control with GitHub

## Common Git commands

```bash
# initialize a git repository: creates a .git file
git init

# clone a git repository 
git clone ...

# add file into staging area
git add ...
git add -a # add all files into staging area

# commit file into repository
git commit -m "message"
# without specifying message here, it will open a text editor for us to write a more complicated commit message
git commit

# push changes into remote repository
git push

# show remote repositories available
git remote -v

# show the git commits in a graph
git log --oneline --graph
git log # more detailed

# checkout to commits: note that it does not save your changes
git checkout commit_id

# creating a new branch and switching to it
git branch branch_name
git checkout branch_name
# shortcut
git checkout -b branch_name

# delete a branch: will warn if branch got changes
git branch -d branch_name

# rename a branch
git branch -m old_branch new_branch

# pulling from remote
git pull
# under the hood, it is actually:
git fetch # fetch from remote repository
git merge # merge the code from remote and your local repository

git status

# difference between a file in a commit id and another commit id
# changes needed to move from commit id_a to commit id_b
git diff id_a id_b

# restore in git
# unstage changes in the staging area, overwrites the index with version from last commit
# but keep your working directory changes
git restore --staged file.txt
# discards changes in working directory by overwriting the file with the version
# from the staging area
git restore file.txt

# switch to a new branch (-c creates it)
git switch -c ...
```