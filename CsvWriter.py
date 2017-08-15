import codecs

class CsvWriter:
    def __init__(self, fileName):
        self.fileName = fileName
        self.separator = ","

    def __enter__(self):
        self.file = codecs.open(self.fileName, 'w', 'utf-8')
        return self

    def add(self, *args):
        row = self.separator.join(args) + '\n'
        self.file.write(row)
        self.file.flush()

    def __exit__(self, exc_type, exc_value, traceback):
        self.file.close()
