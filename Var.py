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

    def __init__(self,r,c,type):
        self.r = r
        self.c = c
        self.type = type
        self.removed_domain = []

    def remaining(self):
        return len(self.domain) - len(self.removed_domain)

    def second_block(self):
        if self.type == 0:
            return (self.r, self.c+1) 
        elif self.type == 1:
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
                if -1 not in self.removed_domain:
                    inferences.append(Inference(self, -1))
            elif charge == -1:
                if 1 not in self.removed_domain:
                    inferences.append(Inference(self, 1))
        else:
            if charge == 1:
                if 1 not in self.removed_domain:
                    inferences.append(Inference(self, 1))
            elif charge == -1:
                if -1 not in self.removed_domain:
                    inferences.append(Inference(self, -1))