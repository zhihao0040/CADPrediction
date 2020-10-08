import sys

def main():
    """
    First argument to script: Name of file to update
    Second argument to script: Name of file to save to
    """
    f = open(sys.argv[1], encoding = "cp437")
    # print(sys.argv[1])
    file_str = f.read()
    # print(file_str)
    f.close()
    # file_str.split("name")
    file_str_newline_removed = file_str.replace("\n"," ")
    # print(file_str_newline_removed)
    file_str_replaced_name_with_new_line = file_str_newline_removed.replace("name ", "\n")
    # print(file_str_replaced_name_with_new_line)
    f = open(sys.argv[2], "w")
    # print(sys.argv[1])
    answer = file_str_replaced_name_with_new_line
    f.write(answer)
    f.close()

main()