# *-* encoding: utf-8 *-*
# This file is part of Project-Stats
# Project-Stats is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# Project-Stats is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Project-Stats. If not, see <http://www.gnu.org/licenses/>.
#
# Source url (https://github.com/LuqueDaniel/ninja-project-stats)

import zipfile
import os
import re

VERSION = "0.5"

FOLDERS = ['project_stats']
PATH_LIST = ['project_stats.plugin']


def get_file_list(path):
    for item in os.listdir(path):
        item_src = os.path.join(path, item)
        if os.path.isdir(item_src):
            get_file_list(item_src)
        elif os.path.isfile(item_src) and not re.search('.+\.pyc$', item):
            PATH_LIST.append(item_src)


with zipfile.ZipFile('ninja-project-stats_{}.zip'.format(VERSION), 'w') as zip_file:
    for folder in FOLDERS:
        get_file_list(os.path.join(folder))
    for item in PATH_LIST:
        zip_file.write(item)

    zip_file.close()
