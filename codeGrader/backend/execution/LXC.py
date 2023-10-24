"""
This file contains the lxc class.
LXC is a Linux Container.
This class will act as a controller for the lxc
@author: mkaiser
"""

import os
import subprocess


class LXC:
    """
    Linux Container Class.
    """
    name: str
    status: str

    def __init__(self, name: str):
        """
        Constructor for the lxc.
        @param name:
        """
        self.name = name
        self.status = "stopped"
        self._lxc_setup()  # creating the lxc

    def _invariant_os(self):
        """
        Invariant method that checks if the os is a posix system.
        This lets the process fail if we do not have a posix system, so we do not attempt to make damage to the OS.
        @return: No Return
        @rtype: None
        """
        assert os.name == 'posix'
        assert int(os.system("lxc-ls")) == 0
        assert self.name is not None
        return True

    def _run_cmd(self, command):
        """
        Runs a subprocess aka Command and only return the text output
        @param command:
        @return:
        """
        result = None
        assert self.name is not None
        p1 = subprocess.run(command, shell=True, text=True, capture_output=True)
        result = p1.stdout
        return result

    def _lxc_get_status(self):
        """
        Getting the status of the LXC and updating the instance variable
        @return: No Return, updates the instance variable
        """
        assert self._invariant_os()
        state = self._run_cmd(f"lxc-info -n {self.name} | grep State")
        self.status = state.replace(" ", "").strip().split(":")[1]

    def _lxc_setup(self):
        """
        Setup an LXC for the Execution
        @return: Nothing
        @rtype: None
        """
        assert self._invariant_os()
        command = f"lxc-create -n {self.name} -t debian -- -r bullseye"
        self._run_cmd(command)

    def _lxc_destroy(self):
        """
        Destroy the LXC after the execution has finished.
        @return: Nothing
        @rtype: None
        """
        assert self._invariant_os()
        command = f"lxc-destroy -n {self.name}"
        self._run_cmd(command)

    def _lxc_start(self):
        """
        Setup an LXC for the Execution
        @return: Nothing
        @rtype: None
        """
        assert self._invariant_os()
        command = f"lxc-start -n {self.name}"
        self._run_cmd(command)

    def _lxc_stop(self):
        """
        Stop the lxc container of the execution
        @return: Nothing
        @rtype: None
        """
        assert self._invariant_os()
        cmd = f"lxc-stop -n {self.name}"
        os.system(cmd)

    def lxc_execute_command(self, command):
        """
        Executes a command on a given LXC Container
        @param command:
        @return:
        """
        assert self._invariant_os()
        command = f"-attach -n {self.name} -- {command}"
        output = self._run_cmd(command)
        return output

    def lxc_upload_file(self, file):
        """
        Upload a file to the lxc container
        @param file: The file to be uploaded
        @return: None
        """
        assert self._invariant_os()
