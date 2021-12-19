from Inference import Inference


class Var(): 
    r = -1
    c = -1
    # 0 - _ horz
    # 1 - | vert
    type = -1
    value = -100
    domain = [0,1,-1]
    removed_domain = None
    constraints = None

    def __init__(self,r,c,type):
        self.r = r
        self.c = c
        self.type = type
        self.removed_domain = [False, False, False]

    def remaining(self):
        # 3 is len(domain)
        return 3 - len(self.removed_domain)

    def second_block(self):
        if self.type == 0:
            return (self.r, self.c+1) 
        elif self:
            return (self.r+1, self.c)
        return None

    def same_col(self):
        r1,c1 = self.second_block()
        return c1 == self.c

    def same_row(self):
        r1,c1 = self.second_block()
        return c1 == self.r

    def revoke_charge_claim(self, r, c, charge, inferences: list):
        r1, c1 = self.second_block()

        if r1 == r and c1 == c:
            if charge == 1:
                if not self.removed_domain[-1+1]:
                    inferences.append(Inference(self, -1))
            elif charge == -1:
                if not self.removed_domain[1+1]:
                    inferences.append(Inference(self, 1))
        else:
            if charge == 1:
                if not self.removed_domain[1+1]:
                    inferences.append(Inference(self, 1))
            elif charge == -1:
                if not self.removed_domain[-1+1]:
                    inferences.append(Inference(self, -1))

    def real_domain(self):
        return list(filter(lambda x: not self.removed_domain[x+1], [0,1,-1]))

    def __neighbor(r, c, r1, c1):
        return (r == r1 and abs(c - c1) == 1) or (c == c1 and abs(r - r1) == 1)

    def first_neighbor(self, r,c):
        return Var.__neighbor(self.r, self.c, r, c)

    def second_neighbor(self, r, c):
        r1, c1 = self.second_block()
        return Var.__neighbor(r1,c1, r, c)