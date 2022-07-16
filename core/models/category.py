class Category:
    id = None
    name = None
    regular_expressions = []

    def __init__(self, id=None, name=None, regular_expressions=[], db_row=None):
        if db_row != None:
            id = db_row[0]
            name = db_row[1]
        self.id = id
        self.name = name
        self.regular_expressions = regular_expressions

    def matches(self, title):
        for regular_expression in self.regular_expressions:
            if regular_expression.matches(title):
                return True
        return False