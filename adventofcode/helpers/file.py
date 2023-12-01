def read_file_as_lines(*, file_path: str) -> list[str]:
    with open(file_path, 'r') as fin:
        content = fin.read()

    return [
        line
        for line in content.split('\n')
        if len(line) > 0
    ]
