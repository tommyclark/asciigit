[![Build Status](https://travis-ci.com/tommyclark/asciigit.svg?token=YfxAsFSSF6uMWM3sNFjo&branch=master)](https://travis-ci.com/tommyclark/asciigit) [![PyPI](https://img.shields.io/pypi/v/asciigit)](https://pypi.org/project/asciigit)

       _            _ _       _ _   
      /_\  ___  ___(_|_) __ _(_) |_ 
     //_\\/ __|/ __| | |/ _` | | __|
    /  _  \__ \ (__| | | (_| | | |_ 
    \_/ \_/___/\___|_|_|\__, |_|\__|
                        |___/       
          
# Asciigit

Asciigit is a terminal UI for [Git](https://git-scm.com). The aim of this project is to make it easier
for you to interact with your Git repositories in the terminal, either
locally or when connected to a remote server over SSH.

## How to open
Navigate to the directory containing the Git repository you want to open, and
run:

```shell
asciigit
```

## How to use
Either use your mouse to click around the terminal interface, or use the tab 
and enter buttons to navigate the screens.

There's also a key binding for ctrl-a that'll open up a shortcuts window.

### Screenshots
Hit enter on a branch to check that branch out.
![terminal git client branch screenshot](assets/branches.png "Asciigit branch window")

View the commit history of your current branch.
![terminal git client commit screenshot](assets/commits.png "Asciigit commits window")

Select the files you want to commit by hitting enter on them,
and then enter a commit message and commit and push at the bottom
of the window.
![terminal git client working copy screenshot](assets/working-copy.png "Asciigit working copy window")

## Installation
You can install this application via [pip](https://pypi.org/project/asciigit):
```
pip install asciigit
```
