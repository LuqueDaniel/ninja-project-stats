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
    This module contain all functions and class for get stats
"""

#OS imports
from os import listdir
from os import path

#RE imports
from re import search
from re import IGNORECASE

#PROJECT-STATS imports
from .resources import IGNORE_FILES
from .resources import IGNORE_FOLDERS
from .resources import IGNORE_FILE_TYPES


class getStats(object):
    """This class get all information.

        Atributes:
                info --> Dictionary with all information.
                projectPath --> Project path.
    """

    def __init__(self, projectPath):
        #Project path
        self.projectPath = projectPath
        #Dictionary with all information
        self.info = {'numberFolders': 0, 'numberFiles': 0, 'numberLines': 0,
                     'numberPyFiles': 0, 'numberPycFiles': 0,
                     'numberPyLines': 0, 'generalFilesLines': {},
                     'pyFilesLines': {}}

        #Run __pathAnalyzer
        self.__pathAnalyzer(self.projectPath)

    def __pathAnalyzer(self, projectPath):
        """Analyze folders and files"""

        listFiles = listdir(projectPath)

        for item in listFiles:
            itemSrc = path.join(projectPath, item)

            if path.isdir(itemSrc):
                if item not in IGNORE_FOLDERS:
                    self.info['numberFolders'] += 1
                    self.__pathAnalyzer(itemSrc)

            elif path.isfile(itemSrc):
                if item not in IGNORE_FILES:
                    self.info['numberFiles'] += 1

                if search('.+\.py$', item):
                    self.info['numberPyFiles'] += 1
                    self.__lineCounter(itemSrc, item, 'numberPyLines')
                elif search('.+\.pyc$', item):
                    self.info['numberPycFiles'] += 1
                elif search(IGNORE_FILE_TYPES, item, IGNORECASE) is None:
                    self.__lineCounter(itemSrc, item)

    def __lineCounter(self, filePath, fileName, dicKey='numberLines'):
        """Counter lines in files"""

        openFile = open(filePath, 'r').readlines()
        self.info['numberLines'] += len(openFile)

        if dicKey == 'numberPyLines':
            self.info['numberPyLines'] += len(openFile)
            self.info['pyFilesLines'][filePath] = {
                'pathInProject': filePath[len(self.projectPath):len(filePath)],
                'lines': len(openFile)}
        else:
            self.info['generalFilesLines'][filePath] = {
                'pathInProject': filePath[len(self.projectPath):len(filePath)],
                'lines': len(openFile)}
