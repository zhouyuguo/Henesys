import os

def get_files(dir_path):
    return_list = list()
    for root, dirs, files in os.walk(dir_path):
        return_list +=  map(lambda x:os.path.join(root, x), files)
    return return_list


def dump(file_content, file_path):
    _dir = os.path.dirname(file_path)
    if not os.path.exists(_dir):
        os.makedirs(_dir)
    with open(file_path, 'w') as fout:
        fout.write(file_content)

