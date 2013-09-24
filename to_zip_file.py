import zipfile
import os
import re

folders = ['project_stats']
path_list = ['project_stats.plugin']


def get_file_list(path):
    for item in os.listdir(path):
        item_src = os.path.join(path, item)
        if os.path.isdir(item_src):
            get_file_list(item_src)
        elif os.path.isfile(item_src) and not re.search('.+\.pyc$', item):
            path_list.append(item_src)


with zipfile.ZipFile('ninja-project-stats.zip', 'w') as zip_file:
    for folder in folders:
        get_file_list(os.path.join(folder))
    for item in path_list:
        zip_file.write(item)

    zip_file.close()
