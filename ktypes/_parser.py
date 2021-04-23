class _parser():
    def __init__(self, ktype, parse_format):
        # TODO: check proper types here

        self.ktype = ktype
        self.parse_format = parse_format
        self._unpack_parse_format()

        self.stream_context = None
        self.stream_tokens = []

    class _unpack_state():
        BASE = 0
        KEYWORD = 1
        
    def _unpack_parse_format(self):
        state = self._unpack_state.BASE
        fragments = []
        fragment = ""

        for c in self.parse_format:
            if c == "$" and state == self._unpack_state.BASE:
                state = self._unpack_state.KEYWORD
                
                # don't add any empty fragments 
                if not fragment:
                    continue

                fragments.append(fragment)
                fragment = ""
                continue

            elif c == "$" and state == self._unpack_state.KEYWORD:
                ktype = self.ktype.dict.get(fragment, None)
                if ktype is None:
                    raise Exception("unknown type keyword")
                fragments.append((fragment, ktype))
                fragment = ""
                state = self._unpack_state.BASE
                continue
                
            fragment = fragment + c

        if fragment:
            fragments.append(fragment)


        self.parse_fragments = fragments

    class _parse_context():
        def __init__(self, fragments):
            self.fragments = fragments
            self.clear()

        def clear(self):
            self.position_in_fragment = 0
            self.fragments_index = 0
            self.current_fragment = self.fragments[0]
            self.fragment_is_str = 1 if isinstance(self.current_fragment, str) else 0
            self.token = ""
            self.elements = {}

        def next_fragment(self):
            self.token = ""
            self.position_in_fragment = 0
            self.fragments_index = self.fragments_index + 1
            if self.fragments_index == len(self.fragments):
                return False

            self.current_fragment = self.fragments[self.fragments_index]

            if isinstance(self.current_fragment, str):
                self.fragment_is_str = True
            else:
                self.fragment_is_str = False

            return True

        def match(self, c, lookahead):
            has_next_fragmnet = True
            if self.fragment_is_str:
                if c != self.current_fragment[self.position_in_fragment]:
                    return {"result": False, "code": "failed to match text delimiter"}

                self.position_in_fragment = self.position_in_fragment + 1

                if self.position_in_fragment == len(self.current_fragment):
                    has_next_fragmnet = self.next_fragment()
            else:
                # proceed by greedy, first-failure-stop, matching
                name, ktype = self.current_fragment
                self.token = self.token + c
                if ktype.matches(self.token) and lookahead is None:
                    self.elements[name] = ktype.construct(self.token)
                    has_next_fragmnet = self.next_fragment()
                elif ktype.matches(self.token) and not ktype.matches(self.token + lookahead):
                    self.elements[name] = ktype.construct(self.token)
                    has_next_fragmnet = self.next_fragment()

            if not has_next_fragmnet:
                return {"result": True, "code": "success", "elements": self.elements}

            return None

    def parse_instance(self, instance):
        context = self._parse_context(self.parse_fragments)
        for i in range(len(instance)):
            lookahead = None if i + 1 == len(instance) else instance[i+1]
            result = context.match(instance[i], lookahead)
            if result is not None:
                return self.ktype.construct(result["elements"])

    def parse_stream(self, stream, reset=False):
        if reset or self.stream_context is None:
            self.stream_context = self._parse_context(self.parse_fragments)
            self.stream_tokens = []

        for i in range(len(stream)):
            lookahead = None if i + 1 == len(stream) else stream[i+1]
            r = self.stream_context.match(stream[i], lookahead)
            if r is not None:
                if r["result"]:
                    self.stream_tokens.append(self.ktype.construct(r["elements"]))
                    self.stream_context.clear()
                else:
                    return result

        return self.stream_tokens