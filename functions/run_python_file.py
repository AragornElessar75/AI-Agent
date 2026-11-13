import os
import subprocess


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    working_dir_abs = os.path.realpath(working_directory)
    target_path = os.path.realpath(os.path.join(working_dir_abs, file_path))
    valid_target_path = os.path.commonpath([working_dir_abs, target_path]) == working_dir_abs

    try:
        if not valid_target_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_path]
        if args is not None:
            command.extend(args)
        process = subprocess.run(command, cwd=working_directory,check=False, capture_output=True, text=True, timeout=30)

        output = ""
        if process.returncode != 0:
            output += f"Process exited with code {process.returncode}"
        if process.stdout == "" and process.stderr == "":
            output += "No output produced"
        else:
            if process.stdout != "":
                output += f"STDOUT: {process.stdout}\n"
            if process.stderr != "":
                output += f"STDERR: {process.stderr}\n"
        return output

    except Exception as e:
        return f"Error: executing Python file: {e}"
