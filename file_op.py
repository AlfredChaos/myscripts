import os


class File():
    def __init__(self, name, path) -> None:
        self.name = name
        self.path = path
        self.abs_path = os.path.join(path, name)

    def create(self):
        if not os.path.isfile(self.abs_path):
            open(self.abs_path, 'w').close()

    def read(self):
        with open(self.abs_path, 'r', encoding='utf-8') as f:
            return f.read()

    def clear(self):
        with open(self.abs_path, 'w') as f:
            f.truncate()
    
    def append(self, content):
        with open(self.abs_path, 'a') as f:
            f.write(content)

    def find(self, keyword):
        with open(self.abs_path, 'r', encoding='utf-8') as f:
            for line_number, line in enumerate(f, 1):
                if keyword in line:
                    return True
        return False
    
    def get_line(self, keyword):
        with open(self.abs_path, 'r', encoding='utf-8') as f:
            for line_number, line in enumerate(f, 1):
                if keyword in line:
                    return line
        return None
    
    def delete_line(self, keyword):
        line_to_keep = []
        with open(self.abs_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        for line in lines:
            if keyword not in line:
                line_to_keep.append(line)
        with open(self.abs_path, 'r', encoding='utf-8') as f:
            f.writelines(line_to_keep)
    
    def modify(self, old, new):
        with open(self.abs_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        for line_number, line in enumerate(lines):
            if old in line:
                lines[line_number] = line.replace(old, new)
                break
        with open(self.abs_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)

