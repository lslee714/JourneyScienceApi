from copy import copy


class AggregateField:
    """Wrappper class to provide convenience in finding a specific field"""
    def __init__(self, *fieldArgs):
        print("PASSED IN ", fieldArgs)
        if not fieldArgs:
            raise TypeError("At least one argument is required")
        self.name = fieldArgs[0]

        self.nestedArgs = fieldArgs[1:]

    @property
    def position(self):
        """The argument to grab a specific element in a nested field"""
        if not self.nestedArgs:
            return None
        firstArg = self.nestedArgs[0]
        if firstArg.isdigit():
            return int(firstArg) - 1
        else:
            return None

    @property
    def nested_fields(self):
        """Nested fields to look at"""
        if self.position is None and self.nestedArgs:
            return self.nestedArgs
        else:
            return self.nestedArgs[1:]
