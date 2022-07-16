import re

class RegularExpression:
    id = None
    content = None

    def __init__(self, id = None, content = None, db_row = None):
        if db_row != None:
            id = db_row[0]
            content = db_row[1]
        self.id = id
        self.content = content

    def matches(self, title):
        pattern = re.compile(self.content)
        return pattern.match(title)