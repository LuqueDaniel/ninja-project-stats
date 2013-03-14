# -*- coding: UTF-8 -*-
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
#Source url (https://github.com/LuqueDaniel/ninja-project-stats)

#NINJA-IDE imports
from ninja_ide.core import plugin

#PyQt4.QtGui imports
from PyQt4.QtGui import QMenu
from PyQt4.QtGui import QDialog
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QTabWidget
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QTableWidgetItem
from PyQt4.QtGui import QTableWidget
from PyQt4.QtGui import QAbstractItemView

#PROJECT-STATS imports
from get_stats import getStats


class projectStatDialog(QDialog):

    def __init__(self, projectInfo):
        super(projectStatDialog, self).__init__()
        self.setWindowTitle('Project Stats - %s' % projectInfo.name)
        self.setMinimumSize(500, 400)
        self.setMaximumSize(0, 0)

        #get project stats --> getStats
        self.projectStats = getStats(projectInfo.path)

        #tabMenu
        self.tabMenu = QTabWidget()

        #LAYOUTS
        #layoutTab
        self.layoutTab = QVBoxLayout()
        self.layoutTab.addWidget(self.tabMenu)

        #==Add layoutTabGeneral
        self.layoutTabGeneral = QVBoxLayout()
        self.layoutTabGeneral.addWidget(QLabel('Number of folders: %i' %
                                    self.projectStats.info['numberFolders']))
        self.layoutTabGeneral.addWidget(QLabel('Number of files: %i' %
                                    self.projectStats.info['numberFiles']))
        self.layoutTabGeneral.addWidget(QLabel('Total number of lines: %i' %
                                    self.projectStats.info['numberLines']))

        #Add table fileTabGeneral at layoutTabGeneral
        self.fileTableGeneral = QTableWidget(0, 2)
        self._configTable(self.fileTableGeneral, 'generalFilesLines')
        self.layoutTabGeneral.addWidget(self.fileTableGeneral)

        #add widget tabGeneral at tabMenu
        self.tabGeneral = QWidget()
        self.tabGeneral.setLayout(self.layoutTabGeneral)
        self.tabMenu.addTab(self.tabGeneral, 'General')

        #==Add layoutTabPy
        #if project contain py files add a py tab
        if self.projectStats.info['numberPyFiles'] != 0:
            self.layoutTabPy = QVBoxLayout()
            self.layoutTabPy.addWidget(QLabel('Number of .py files: %i' %
                                    self.projectStats.info['numberPyFiles']))
            self.layoutTabPy.addWidget(QLabel('Number of .pyc files: %i' %
                                    self.projectStats.info['numberPycFiles']))
            self.layoutTabPy.addWidget(QLabel('Total number of lines: %i' %
                                    self.projectStats.info['numberPyLines']))

            #add table fileTablelist at layoutTabPy
            self.fileTablePy = QTableWidget(10, 2)
            self._configTable(self.fileTablePy, 'pyFilesLines')
            self.layoutTabPy.addWidget(self.fileTablePy)

            #add Widget TabPy at tabMenu
            self.tabPy = QWidget()
            self.tabPy.setLayout(self.layoutTabPy)
            self.tabMenu.addTab(self.tabPy, '.py')

        #Vertical Layout
        self.vLayout = QVBoxLayout(self)
        self.vLayout.setContentsMargins(15, 10, 15, 10)
        #add label with project name
        self.vLayout.addWidget(QLabel('<b>Project name:</b> %s' %
                                projectInfo.name))
        #add tabMenu
        self.vLayout.addLayout(self.layoutTab)

    def _configTable(self, table, dictKey):
        self.tableHeaders = ('Name', 'Number of lines')
        table.setRowCount(len(self.projectStats.info[dictKey]))
        table.setHorizontalHeaderLabels(self.tableHeaders)
        #No edit items
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        #Single selection
        table.setSelectionMode(QTableWidget.SingleSelection)
        #Select all columns
        table.setSelectionBehavior(QAbstractItemView.SelectRows)
        #Expand columns
        table.horizontalHeader().setStretchLastSection(True)
        #Set width of columns
        table.setColumnWidth(0, 250)

        row = 0
        for item in list(self.projectStats.info[dictKey].items()):
            table.setItem(row, 0, QTableWidgetItem(item[0]))
            table.setItem(row, 1, QTableWidgetItem(str(item[1])))

            row += 1


class projectStatsMain(plugin.Plugin):

    def initialize(self):
        #Create plugin menu
        self.menu = QMenu()
        self.menu.setTitle('Project Stats')
        self.menu.addAction('Project Stats', lambda: self.projectStatAction())

        #Add Project Stats menu
        self.ex_locator = self.locator.get_service('explorer')
        self.ex_locator.add_project_menu(self.menu)

    def projectStatAction(self):
        #Get project properties
        self.currentProject = self.ex_locator.get_tree_projects()._get_project_root()

        #Instance projectStatDialog
        self.projectStatDialog = projectStatDialog(self.currentProject)
        self.projectStatDialog.show()
