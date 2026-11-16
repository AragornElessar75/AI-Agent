import os


def write_file(working_directory: str, file_path: str, content: str) -> str:
    working_dir_abs = os.path.realpath(working_directory)
    target_path = os.path.realpath(os.path.join(working_dir_abs, file_path))
    valid_target_path = os.path.commonpath([working_dir_abs, target_path]) == working_dir_abs

    try:
        if not valid_target_path:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        os.makedirs(os.path.dirname(target_path), exist_ok=True)

        with open(target_path, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "write content to one file from given file_path",
        "parameters": {
            "type": "object",
            "required": ["file_path", "content"],
            "properties": {
                "file_path":{
                "type": "string",
                    "description": "write content to file from given file_path",
                },
                "content": {
                "type": "string",
                    "description": "content to be written to file",
                },
            },
        },
    },
}
