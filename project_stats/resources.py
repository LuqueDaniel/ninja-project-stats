# -*- coding: utf-8 -*-
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

"""
    This module contain resources for project-stats.

    Attributes:
        IGNORE_FOLDERS: Ignore folders.
        IGNORE_FILES: Ignore files.
        IGNORE_FILE_TYPES: String to ignore file extensions.
"""

#Tupla to ignore folders
IGNORE_FOLDERS = ('.git', '_MACOSX')

#Tupla to ignore files
IGNORE_FILES = ('Thumbs.db')

#Tupla to ignore file extensions
re_file_types = ('.+(', '\.pyc|', '\.py|', '\.mkv|', '\.mp3|', '\.db|',
                 '\.psd|', '\.doc|', '\.pdf|', '\.bmp|', '\.png|', '\.ico|',
                 '\.gif|', '\.jpg|', '\.jpeg|', '\.xcf|', '\.swf|', '\.zip|',
                 '\.rar|', '\.iso|', '\.dll|', '\.exe', ')$')

IGNORE_FILE_TYPES = ''.join(re_file_types)
