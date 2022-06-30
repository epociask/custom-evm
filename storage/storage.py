class Storage:

    l = {}

    def set(self, slot_loc: int, item: int):
        self.l[slot_loc] = item

    def get(self, slot_loc: int):
        return self.l[slot_loc]