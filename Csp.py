from Inference import Inference
from Var import Var

class Csp():
    rows = -1
    cols = -1
    row_vals = None
    col_vals = None
    row_nvals = None
    col_nvals = None
    data: "list[list[int]]" = None
    mp: "list[list[list[Var]]]" = None
    variables = None
    
    def __init__(self, rows, cols, row_vals, col_vals, row_nvals, col_nvals, data, mp, variables):
        self.rows = rows
        self.cols = cols
        self.row_vals = row_vals
        self.col_vals = col_vals
        self.row_nvals = row_nvals
        self.col_nvals = col_nvals
        self.data = data
        self.mp = mp
        self.variables = variables

    def claim(self, r, c, inferences: list):
        var = self.mp[r][c]
        if -1 not in var.removed_domain:
            inferences.append(Inference(var, -1))
        if 1 not in var.removed_domain:
            inferences.append(Inference(var, 1))

    def claim_charge(self, r, c, charge, inferences: list):

        #left
        if c-1 >= 0:
            var = self.mp[r][c-1]
            var.revoke_charge_claim(r, c-1, charge, inferences)

        #right
        if c+1 < self.cols:
            var = self.mp[r][c+1]
            var.revoke_charge_claim(r, c+1, charge, inferences)
        #up
        if r-1 >= 0:
            var = self.mp[r-1][c]
            var.revoke_charge_claim(r-1, c, charge, inferences)
        #down
        if r+1 < self.rows:
            var = self.mp[r+1][c]
            var.revoke_charge_claim(r+1, c, charge, inferences)

    def append(self, var: Var, value: int):
        r1, c1 = var.second_block()
        v1, v2 = ('e', 'e')

        if value == 1:
            v1 = '+'
            v2 = '-'
        elif value == -1:
            v1 = '-'
            v2 = '+'

        var.value = value
        self.data[var.r][var.c] = v1
        self.data[r1][c1] = v2

    def append_inferences(self, inferences: "list[Inference]"):
        for i in inferences:
            if i.val not in i.var.removed_domain:
                i.var.removed_domain.append(i.val)

    def remove(self, var: Var, value: int):
        r1, c1 = var.second_block()
        var.value = -100
        if var.type == 0:
            self.data[var.r][var.c] = 'l'
            self.data[r1][c1] = 'r'
        if var.type == 1:
            self.data[var.r][var.c] = 'u'
            self.data[r1][c1] = 'd'

    def remove_inferences(self, inferences: "list[Inference]"):
        for i in inferences:
            if i.val in i.var.removed_domain:
                i.var.removed_domain.remove(i.val)

    def print(self):
        for i in range(self.rows):
            for j in range(self.cols):
                print(self.data[i][j], end=' ')
            print()
        print()