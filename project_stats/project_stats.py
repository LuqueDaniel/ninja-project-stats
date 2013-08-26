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

        #get project stats --> getStats
        self.projectStats = getStats(projectInfo.path)

        #tabMenu
        tabMenu = QTabWidget()
        tabMenu.tabCloseRequested.connect(tabMenu.removeTab)
        tabMenu.setMovable(True)
        tabMenu.setTabsClosable(True)

        #LAYOUTS
        #layoutTab
        layoutTab, layoutTabGeneral = QVBoxLayout(), QVBoxLayout()
        layoutTab.addWidget(tabMenu)

        #Add table fileTabGeneral at layoutTabGeneral
        fileTableGeneral = QTableWidget(0, 2)
        self._configTable(fileTableGeneral, 'generalFilesLines')

        for each_widget in (
            QLabel('Number of folders: {}'.format(self.projectStats.info['numberFolders'])),
            QLabel('Number of files: {}'.format(self.projectStats.info['numberFiles'])),
            QLabel('Total number of lines: {}'.format(self.projectStats.info['numberLines'])),
            fileTableGeneral):
            layoutTabGeneral.addWidget(each_widget)

        #add widget tabGeneral at tabMenu
        tabGeneral, tabPy = QGroupBox(), QGroupBox()
        tabGeneral.setLayout(layoutTabGeneral)
        tabMenu.addTab(tabGeneral, 'General')

        #==Add layoutTabPy
        #if project contain py files add a py tab
        if self.projectStats.info['numberPyFiles'] != 0:
            layoutTabPy = QVBoxLayout()

            #add table fileTablelist at layoutTabPy
            fileTablePy = QTableWidget(10, 2)
            self._configTable(fileTablePy, 'pyFilesLines')

            for each_widget in (
                QLabel('Number of .py files: {}'.format(self.projectStats.info['numberPyFiles'])),
                QLabel('Number of .pyc files: {}'.format(self.projectStats.info['numberPycFiles'])),
                QLabel('Total number of lines: {}'.format(self.projectStats.info['numberPyLines'])),
                fileTablePy):
                layoutTabPy.addWidget(each_widget)

            #add Widget TabPy at tabMenu
            tabPy.setLayout(layoutTabPy)
            tabMenu.addTab(tabPy, '.py')

        #Vertical Layout
        vLayout = QVBoxLayout(self)
        vLayout.setContentsMargins(15, 10, 15, 10)
        #add label with project name
        vLayout.addWidget(QLabel('<b>Project name:</b> {}'.format(
                                                            projectInfo.name)))
        #add tabMenu
        vLayout.addLayout(layoutTab)

    def _configTable(self, table, dictKey):
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
        menu.addAction('Project Stats', lambda: self.projectStatAction())

        #Add Project Stats menu
        self.ex_locator = self.locator.get_service('explorer')
        self.ex_locator.add_project_menu(menu)

    def projectStatAction(self):
        """Init projectStatsDialog"""

        #Get project properties
        self.currentProject = self.ex_locator.get_tree_projects()._get_project_root()

        #Instance projectStatDialog
        self.projectStatsDialog = projectStatsDialog(self.currentProject)
        self.projectStatsDialog.show()
