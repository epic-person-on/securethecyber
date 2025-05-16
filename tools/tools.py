import subprocess
from langchain.agents import tool

@tool
def bash(command: str) -> str:
    """Run a shell command and return the output."""
    try:
        result = subprocess.run(
            "bash tools/command.sh '"+command+"'", shell=True, check=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        return result.stdout + result.stderr
    except subprocess.CalledProcessError as e:
        return f"Command failed with error:\n{e.stderr}"

@tool
def clamav(directory: str) -> str:
    """Run a ClamAV scan on a directory"""
    try:
        output = bash(f"clamscan -r '{directory}'")
        summary_start = output.find("----------- SCAN SUMMARY -----------")
        if summary_start != -1:
            summary = output[summary_start:].strip()
            return summary
        else:
            return "Scan summary not found in the output."

    except FileNotFoundError:
        return "clamscan command not found. Is ClamAV installed?"

