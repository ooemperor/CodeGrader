# CodeGrader - https://github.com/ooemperor/CodeGrader
# Copyright © 2023, 2024 Michael Kaiser <michael.kaiser@emplabs.ch>
#
# This file is part of CodeGrader.
#
# CodeGrader is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# CodeGrader is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with CodeGrader.  If not, see <http://www.gnu.org/licenses/>.

from setuptools import setup, find_packages

PACKAGE_DATA = {
    "codeGrader.frontend": [
        "admin/static/*",
        "admin/static/*/*",
        "admin/static/*/*/*",
        "admin/templates/*.*",
        "user/static/*",
        "user/static/*/*",
        "user/static/*/*/*",
        "user/templates/*.*"
    ]
}

setup(
    name='codeGrader',
    version='1.0',
    packages=find_packages(exclude=["*backend*"]),
    package_data=PACKAGE_DATA,
    url='https://github.com/ooemperor/CodeGrader',
    license='GNU Affero General Public License v3.0',
    author='mkaiser',
    author_email='michael.kaiser@emplabs.ch',
    description='A WebApplication for automated code execution and evaluation called CodeGrader',
    entry_points={
        'console_scripts': [
            'cgAdminFrontend = codeGrader.scripts.cgAdminFrontend:main',
            'cgUserFrontend = codeGrader.scripts.cgUserFrontend:main'
        ]
    }
)
