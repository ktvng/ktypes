from ktypes._abstract_type import KType
from ktypes._token import _Token

# represents a coproduct (or) type from two component types 
class kor(KType):
    instances = {}

    def __init__(self, universe, left, right, predicate=None):
        super().__init__(universe, predicate=predicate)
        self.name = str(left) + " | " + str(right) 
        self.left = left
        self.right = right

    def where(self, predicate):
        self.predicate = predicate
        return self

    def matches(self, raw_data):
        return self.left.matches(raw_data) or self.right.matches(raw_data)

    def construct(self, raw_data):
        if self.left.matches(raw_data):
            return self._inl(self.left.construct(raw_data))
        elif self.right.matches(raw_data):
            return self._inr(self.right.construct(raw_data))

    def _inl(self, token):
        return _Token(("inl", token), self)

    def _inr(self, token):
        return _Token(("inr", token), self)
