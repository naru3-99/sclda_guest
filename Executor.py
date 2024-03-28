# 2023/09/19
# auther:naru
# encoding=utf-8

from lib.fs import (
    get_all_file_path_in,
    get_file_name,
    get_parent_directory,
    get_file_extension,
)
from lib.multp import parallel_process

from execute_program import execute_java_file, execute_python_file
from UDPClient import UDPClient
from CONST import HOST, PORT, TARGET_PATH

client = UDPClient()


def run_program(path):
    current_dir = get_parent_directory(path)
    file_name = get_file_name(path)
    file_extension = get_file_extension(path)
    ret = (None, None, None, None)

    try:
        if file_extension == ".py":
            ret = execute_python_file(current_dir, file_name)
        elif file_extension == ".java":
            ret = execute_java_file(current_dir, file_name)
        else:
            return
        # "pid,file_name,return code"
        client.send_message(
            HOST,
            PORT,
            f"{ret[1]},{file_name},{ret[0]}",
            encoding="utf-8",
        )
    except:
        client.send_message(HOST, PORT, f"None,{file_name},None", encoding="utf-8")


if __name__ == "__main__":
    parallel_process(run_program, get_all_file_path_in(TARGET_PATH))
