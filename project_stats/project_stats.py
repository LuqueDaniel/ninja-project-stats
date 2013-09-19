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
# Source url (https://github.com/LuqueDaniel/ninja-project-stats)

"""
    This module contain the main function of the plugin.
"""

#NINJA-IDE imports
from ninja_ide.core import plugin

#PyQt4.QtGui imports
from PyQt4.QtGui import (QMenu, QDialog, QLabel, QVBoxLayout, QTabWidget,
    QTableWidgetItem, QTableWidget, QAbstractItemView, QGroupBox)

#PROJECT-STATS imports
from .get_stats import getStats


class projectStatsDialog(QDialog):
    """This class show project stats in a QDialog.

    init Parameters:
        projectInfo: Information of the current project.

    Attributes:
        projectStats: Contain stats of the project.
    """

    def __init__(self, projectInfo):
        ' init projectStatsDialog class '
        super(projectStatsDialog, self).__init__()
        self.setWindowTitle('Project Stats - {}'.format(projectInfo.name))
        self.setMinimumSize(500, 400)
        self.setMaximumSize(0, 0)

        #List contain the text of labels.
        self.textLabels = ['Number of folders: {}', 'Number of files: {}',
                           'Total number of lines: {}', 'Number of .py files: {}',
                           'Number of .pyc files: {}', 'Total number of lines: {}']

        #get project stats --> getStats
        self.projectStats = getStats(projectInfo.path)

        #Create tabMenu
        tabMenu = QTabWidget()
        tabMenu.tabCloseRequested.connect(tabMenu.removeTab)
        tabMenu.setMovable(True)
        tabMenu.setTabsClosable(True)

        #Create labels for tabGeneral
        self.generalNumberFolders = QLabel(self.textLabels[0].format(self.projectStats.info['numberFolders']))
        self.generalNumberFiles = QLabel(self.textLabels[1].format(self.projectStats.info['numberFiles']))
        self.generalNumberLines = QLabel(self.textLabels[2].format(self.projectStats.info['numberLines']))

        #Create tablefilesgeneral
        tableFilesGeneral = QTableWidget(0, 2)
        self.__configTable(tableFilesGeneral, 'generalFilesLines')

        #LAYOUTS
        #==Create central layout
        vLayout = QVBoxLayout(self)
        vLayout.setContentsMargins(15, 10, 15, 10)
        #add label with project name
        vLayout.addWidget(QLabel('<b>Project name:</b> {}'.format(
                                                            projectInfo.name)))
        #==Create layoutTabGeneral and layoutTabs
        layoutTabGeneral, layoutTabs = QVBoxLayout(), QVBoxLayout()

        #Add widgets to layoutTabGeneral
        for each_widget in (self.generalNumberFolders, self.generalNumberFiles,
                            self.generalNumberLines, tableFilesGeneral):
            layoutTabGeneral.addWidget(each_widget)

        #==Create tabGeneral
        tabGeneral = QGroupBox()
        tabGeneral.setLayout(layoutTabGeneral)

        #Add tabGeneral to tabMenu
        tabMenu.addTab(tabGeneral, 'General')

        #==if project contain py files add a tab
        if self.projectStats.info['numberPyFiles'] != 0:
            #Create layoutTabPy
            layoutTabPy = QVBoxLayout()

            #Create labels for tabPy
            self.pyNumberFiles = QLabel(self.textLabels[3].format(self.projectStats.info['numberPyFiles']))
            self.pyNumberFilesPyc =QLabel(self.textLabels[4].format(self.projectStats.info['numberPycFiles']))
            self.pyNumberLines = QLabel(self.textLabels[5].format(self.projectStats.info['numberPyLines']))

            #Create table tableFilesPy
            tableFilesPy = QTableWidget(10, 2)
            self.__configTable(tableFilesPy, 'pyFilesLines')

            #Add widgets to layoutTabPy
            for each_widget in (self.pyNumberFiles, self.pyNumberFilesPyc,
                                self.pyNumberLines, tableFilesPy):
                layoutTabPy.addWidget(each_widget)

            #Create tabPy
            tabPy = QGroupBox()
            tabPy.setLayout(layoutTabPy)

            #add Widget TabPy to tabMenu
            tabMenu.addTab(tabPy, '.py')

        #Add tabMenu to layoutTabs
        layoutTabs.addWidget(tabMenu)

        #add tabMenu
        vLayout.addLayout(layoutTabs)

    def __configTable(self, table, dictKey):
        """This function configure a table.

        Parameters:
            table: Table to configure.
            dictKey: The dictKey.
        """

        self.tableHeaders = ('Path & File name', 'Number of lines')
        table.setRowCount(len(self.projectStats.info[dictKey]))
        table.setHorizontalHeaderLabels(self.tableHeaders)
        #Disable edit items
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
            table.setItem(row, 0, QTableWidgetItem(item[1]['pathInProject']))
            table.setItem(row, 1, QTableWidgetItem(str(item[1]['lines'])))
            row += 1


class projectStatsMain(plugin.Plugin):
    """Main class of the plugin.

    Attributes:
        ex_locator: ninja-ide explorer service.
    """

    def initialize(self):
        """This function start plugin"""

        #Create plugin menu
        menu = QMenu('Project Stats')
        menu.addAction('Project Stats', lambda: self.projectStatsMenuAction())

        #Add Project Stats menu
        self.ex_locator = self.locator.get_service('explorer')
        self.ex_locator.add_project_menu(menu)

    def projectStatsMenuAction(self):
        """Init projectStatsDialog"""

        #Get project properties
        self.currentProject = self.ex_locator.get_tree_projects()._get_project_root()

        #Instance projectStatDialog
        self.projectStatsDialog = projectStatsDialog(self.currentProject)
        self.projectStatsDialog.show()
