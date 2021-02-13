from github import Github
import pandas as pd
from os import listdir
import sys
import datetime

g = Github("848013873a5d37a03ea9a1a133daf05d1cae3b86")
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
filenames = find_csv_filenames("/Users/vedangjoshi/PycharmProjects/formulaj/driver_stats")
for name in filenames:
  file_list.append(name)

name_list = []
for i in file_list:
    name_list.append(i.split('_')[0])

print(name_list)

markdowntextinit = '''---
layout: post 
title: %s Driver Statistics
--- 

'''
for i in range(len(name_list)):
    df_driver_stat = pd.read_csv("/Users/vedangjoshi/PycharmProjects/formulaj/driver_stats/" + file_list[i])
    df_driver_stat = df_driver_stat.set_index('Season')

    markdown_df_drivers = df_driver_stat.to_markdown()
    markdowndfwithtxt = markdowntextinit % (name_list[i]) + markdown_df_drivers

    git_file = '%s_page.md'%(name_list[i])
    if git_file in all_files:
        contents = repo.get_contents(git_file)
        repo.update_file(contents.path, "committing files", markdowndfwithtxt, contents.sha, branch="master")
        print(git_file + ' UPDATED')
    else:
        repo.create_file(git_file, "committing files", markdowndfwithtxt, branch="master")
        print(git_file + ' CREATED')
