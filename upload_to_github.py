from github import Github
import pandas as pd
from os import listdir
import sys
import datetime

print("The program will ask you to input dates in the format yyyy-mm-dd for when the season took place.")
print("This data will be used to generate and order filenames on Github")
print("To exit out of entering data - input 'finish'. This command is case sensitive")

def validate(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")


# Ask user inputs for dates:
# Example given below:
#date_list = ['2020-10-01']
date_list = []
for i in range(100000000000000):
    i = i+1
    date = input("Enter date for season %d: " %i)
    date_list.append(date)
    if type(date) == list:
        date_list = date
        break
    if date_list[0] == 'finish':
        quit()
    elif date == 'finish':
        break
    else:
        try:
            validate(date)
        except ValueError:
            print("NumericError: Please enter numeric entries for the date in the format YYYY-MM-DD. To exit "
                  "out of the program safely, enter 'finish'", file=sys.stderr)
            quit()


g = Github("7c8459971ea07bd6cb1e091635d5a438520f6cf3")
repo = g.get_user().get_repo("formulaj.github.io")

all_files = []
contents = repo.get_contents("")
while contents:
    file_content = contents.pop(0)
    if file_content.type == "dir":
        contents.extend(repo.get_contents(file_content.path))
    else:
        file = file_content
        all_files.append(str(file).replace('ContentFile(path="','').replace('")',''))


def find_csv_filenames( path_to_dir, suffix=".csv" ):
    filenames = listdir(path_to_dir)
    return [filename for filename in filenames if filename.endswith( suffix )]

file_list = []
filenames = find_csv_filenames("/Users/vedangjoshi/PycharmProjects/formulaj")
for name in filenames:
  file_list.append(name)


# write markdown text here initialise the .md files
markdowntextdrivers = '''---
layout: post 
title: Season %s 
summary: This post contains all the information relating to Season %s of Formula j! 
featured-img: sleek 
--- 
Drivers Championship

'''

markdowntextteams = '''


Teams Championship

'''


count_file = 0
count_date = 0
while True:
    try:
        season_num = list(file_list[count_file])[1]

        df_drivers = pd.read_csv(file_list[count_file])
        df_teams = pd.read_csv(file_list[count_file+1])
        df_drivers = df_drivers.set_index('Pos')
        df_teams = df_teams.set_index('Pos')
        markdown_df_drivers = df_drivers.to_markdown()
        markdown_df_teams = df_teams.to_markdown()
        markdowndfwithtxt = markdowntextdrivers % (season_num, season_num) + markdown_df_drivers + markdowntextteams + markdown_df_teams

        # Upload to github
        git_prefix = '_posts/'
        git_file = git_prefix + '%s-season-%s.md'%(date_list[count_date], season_num)
        if git_file in all_files:
            contents = repo.get_contents(git_file)
            repo.update_file(contents.path, "committing files", markdowndfwithtxt, contents.sha, branch="master")
            print(git_file + ' UPDATED')
        else:
            repo.create_file(git_file, "committing files", markdowndfwithtxt, branch="master")
            print(git_file + ' CREATED')

        count_file = count_file + 2
        count_date = count_date + 1
    except IndexError:
        break
