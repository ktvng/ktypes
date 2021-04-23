from ktypes._abstract_type import KType

class knone(KType):
    instances = {}

    def __init__(self):
        super().__init__()
        self.name = "None"

    def construct(self, raw_data):
        raise Exception("cannot construct token of KType.None")
    
    def matches(self, raw_data):
        raise Excpetion("cannot match token of KType.None")




