
import subprocess
import os

command = "dir"
def run():
    p1 = subprocess.run(command, shell=True, text=True, capture_output=True)
    output = p1.stdout
    returncode = p1.returncode
    return output, returncode

x, y = run()

print(x)