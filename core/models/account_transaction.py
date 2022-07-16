class AccountTransaction:
    id = None
    nordigen_transaction_id = None
    title = None
    date = None
    amount = None
    create_date = None
    last_edit_date = None
    source = None
    category = None

    def __init__(
        self,
        id = None,
        nordigen_transaction_id = None,
        title = None,
        date = None,
        amount = None,
        create_date = None,
        last_edit_date = None,
        source = None,
        category = None,
        nordigen_transaction = None
    ):
        if nordigen_transaction != None:
            nordigen_transaction_id = nordigen_transaction.id
            title = nordigen_transaction.title
            amount = nordigen_transaction.amount
            date = nordigen_transaction.date
            source = nordigen_transaction.source
        self.id = id
        self.nordigen_transaction_id = nordigen_transaction_id
        self.title = title
        self.date = date
        self.amount = amount
        self.create_date = create_date
        self.last_edit_date = last_edit_date
        self.source = source
        self.category = category

    def attach_category(self, categories):
        for category in categories:
            if category.matches(self.title):
                self.category = category
                return