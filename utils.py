import subprocess
import os

DIR = os.path.abspath(os.path.dirname(__file__))
SCRIPTS_DIR = os.path.join(DIR, "scripts")

def get_cpu_usage():
    output = subprocess.check_output([os.path.join(SCRIPTS_DIR, "cpu_usage.sh")])
    return output.strip()


def get_mem_usage():
    output = subprocess.check_output([os.path.join(SCRIPTS_DIR, "mem_usage.sh")])
    return output.strip()


def get_kernel():
    output = subprocess.check_output(
        "uname -a",
        shell=True
    )
    return output.strip()
