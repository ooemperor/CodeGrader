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

"""
This file contains the lxc class.
LXC is a Linux Container.
This class will act as a controller for the lxc
@author: mkaiser
"""

import os
import subprocess
from codeGrader.backend.config import config


class LXC:
    """
    Linux Container Class.
    """
    name: str
    status: str
    ip: str

    def __init__(self, name: str):
        """
        Constructor for the lxc.
        @param name:
        """
        self.name = name
        self.status = "stopped"
        self.ip = None
        self._lxc_setup()  # creating the lxc

    def _invariant_os(self):
        """
        Invariant method that checks if the os is a posix system.
        This lets the process fail if we do not have a posix system, so we do not attempt to make damage to the OS.
        @return: No Return
        @rtype: None
        """
        assert os.name == 'posix'
        assert self.name is not None
        output, exitcode = self._run_cmd("lxc-ls")
        assert exitcode == 0
        return True

    def lxc_execute_command(self, command: str):
        """
        Executes a command on a given LXC Container
        @param command:
        @return:
        """
        assert self._invariant_os()
        command = f"lxc-attach -n {self.name} -- /bin/bash -c '{command}'"
        output, returncode = self._run_cmd(command)
        return output, returncode

    def _run_cmd(self, command):
        """
        Runs a subprocess aka Command and only return the text output
        @param command: The command that shall be executed
        @type command: str
        @return: Output of the Execution, Returncode of the execution
        @rtype: str, int
        """
        result = None
        assert self.name is not None
        p1 = subprocess.run(command, shell=True, text=True, capture_output=True)
        output = p1.stdout
        returncode = p1.returncode

        return output, returncode

    def lxc_get_info(self):
        """
        Getting the status of the LXC and updating the instance variable
        @return: No Return, updates the instance variable
        """
        assert self._invariant_os()

        try:
            # if there is no ip or the container does not yet exist, we do not update the values
            # needed so we can wait to install packages after the container has gotten an ip adress.
            state, returncode = self._run_cmd(f"lxc-info -n {self.name} -s")
            ip, returncode = self._run_cmd(f"lxc-info -n {self.name} -i")
            self.status = state.replace(" ", "").strip().split(":")[1]
            self.ip = ip.replace(" ", "").strip().split(":")[1]
        except IndexError as error:
            pass  # do nothing

    def _lxc_setup(self):
        """
        Setup an LXC for the Execution
        @return: Nothing
        @rtype: None
        """
        assert self._invariant_os()
        command = f"lxc-create -n {self.name} {config.execution_LXC_Install_Command}"
        self._run_cmd(command)

    def lxc_destroy(self):
        """
        Destroy the LXC after the execution has finished.
        @return: Nothing
        @rtype: None
        """
        assert self._invariant_os()
        command = f"lxc-destroy -n {self.name}"
        self._run_cmd(command)

    def lxc_start(self):
        """
        Setup an LXC for the Execution
        @return: Nothing
        @rtype: None
        """
        assert self._invariant_os()
        command = f"lxc-start -n {self.name}"
        self._run_cmd(command)
        self.lxc_get_info()

    def lxc_stop(self):
        """
        Stop the lxc container of the execution
        @return: Nothing
        @rtype: None
        """
        assert self._invariant_os()
        assert self.status != 'stopped'
        cmd = f"lxc-stop -n {self.name}"
        self._run_cmd(cmd)
        self.lxc_get_info()

    def lxc_upload_file(self, filePath: str, fileName: str, fileContent):
        """
        Upload/Copy/Create a file in the directory of the LXC.
        @param filePath: The path where the file shall be stored.
        @type filePath: str
        @param fileName: The name of the file that shall be written
        @type fileName: file
        @param fileContent: The content of the filename that has been converted to normal string and is not Bytes anymore
        @type fileContent: String
        @return: None
        """
        assert self._invariant_os()
        assert fileName is not None
        assert type(fileName) is str
        assert fileContent is not None

        nf = open(f'/var/lib/lxc/{self.name}/rootfs{filePath}/{fileName}', 'wb')
        data = fileContent
        nf.write(data)
        nf.close()
