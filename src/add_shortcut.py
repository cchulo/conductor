import os


def add_shortcut(path: str) -> int:
    print(f'adding {path} to steam...')
    expanded_path = os.path.expanduser(path)
    # check to make sure expanded_path is a full path
    if not os.path.isabs(expanded_path):
        print(f'path {path} is not a full path')
        return 1
    

    pass
