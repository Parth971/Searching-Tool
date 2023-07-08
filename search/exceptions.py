from search.constants import EMPTY_QUERY_EXCEPTION_MSG


class EmptyQueryException(Exception):
    def __init__(self, message=EMPTY_QUERY_EXCEPTION_MSG):
        self.message = message
        super().__init__(self.message)
