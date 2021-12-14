from Assignment import Assignment
from Csp import Csp
from Inference import Inference
from Var import Var


class BackTrack():
    csp = None
    rows = None
    cols = None
    # test = None
    # test1 = None
    # test2 = None
    # test3 = None
    # test4 = None
    # test5 = None
    # test6 = None
    # test7 = None
    # test8 = None
    # test9 = None
    
    def __init__(self, csp: Csp):
        self.csp = csp
        self.rows = range(csp.rows)
        self.cols = range(csp.cols)

    #Returns a solution or failure
    def search(self):
        return self.backtrack(Assignment(self.csp.rows, self.csp.cols))

    #Returns a solution or failure
    def backtrack(self, assignment: Assignment):
        if self.complete(assignment):
            return assignment

        var = self.select_unassigned_variable(assignment)
        # if var is None:
        #     print('None')
        # else:
        #     
        for value in self.order_domain_values(var, assignment):
            #print('r:%d c:%d value: %d' % (var.r, var.c, value))
            if self.consistent(var, value, assignment):
                self.csp.append(var, value)
                # if self.test.value == -1 and self.test1.value == 1 and self.test2.value == 1 and self.test3.value == 1 and self.test4.value == 1 and self.test5.value == 1 and self.test6.value == 1 and self.test7.value == 1:
                #     print(self.test8.removed_domain)
                #     self.csp.print()
                inferences = self.inference(var,value, assignment)
                if inferences != 'failure':
                    self.csp.append_inferences(inferences)
                    result = self.backtrack(assignment)
                    if result != 'failure':
                        return result
                    self.csp.remove_inferences(inferences)
                self.csp.remove(var, value)
        return 'failure'

    def select_unassigned_variable(self, assignment: Assignment):
        unassigned = list(filter(lambda x : x.value == -100 ,self.csp.variables))
        if len(unassigned) == 0:
            return None
        min = unassigned[0]

        for var in unassigned:
            if var == min:
                continue
            r = var.remaining()
            n = min.remaining()

            if r < n:
                min = var
                if min.remaining() == 1:
                    return min
            #else if r= n

        return min
                
    def complete(self, assignment: Assignment):
        #Check the first row, get sum of +, sum of -, check rules, so on...
        for i in range(self.csp.rows):
            plus_sum = 0
            neg_sum = 0
            for j in range(0, self.csp.cols):
                if self.csp.data[i][j] == '+':
                    plus_sum += 1
                elif self.csp.data[i][j] == '-':
                    neg_sum += 1
            if plus_sum != self.csp.row_vals[i]:
                return False
            if neg_sum != self.csp.row_nvals[i]:
                return False

        #Like before, just do it for columns
        for j in range(self.csp.cols):
            plus_sum = 0
            neg_sum = 0
            for i in range(0, self.csp.rows):
                if self.csp.data[i][j] == '+':
                    plus_sum += 1
                elif self.csp.data[i][j] == '-':
                    neg_sum += 1
            if plus_sum != self.csp.col_vals[j]:
                return False
            if neg_sum != self.csp.col_nvals[j]:
                return False

        return True

    def order_domain_values(self, var: Var, assignment: Assignment):
        if var is None:
            return []
        return list(filter(lambda x: x not in var.removed_domain, [0,1,-1]))

    def consistent(self, var: Var, value, assignment: Assignment):
        return True
        
    def inference(self, var: Var, value, assignment):


        # It blocks some
        inferences = []
        self.csp.claim(var.r, var.c, inferences)
        r1,c1 = var.second_block()
        self.csp.claim(r1,c1, inferences)
        # It stops some from being same charge
        if value != 0:
            self.csp.claim_charge(var.r, var.c, value, inferences)
            self.csp.claim_charge(r1,c1, -1*value, inferences)

        rows = set()
        cols = set()
        for i in inferences:
            rows.add(i.var.r)
            cols.add(i.var.c)
        self.rows = rows
        self.cols = cols

        for i in self.rows:
            plus_sum = 0
            neg_sum = 0
            plus_candids = 0
            neg_candids = 0
            for j in range(0, self.csp.cols):
                if self.csp.data[i][j] == '+':
                    plus_sum += 1
                elif self.csp.data[i][j] == '-':
                    neg_sum += 1
                elif self.csp.data[i][j] == 'l' or self.csp.data[i][j] == 'u':
                    if 1 not in self.csp.mp[i][j].removed_domain:
                        plus_candids += 1
                    if -1 not in self.csp.mp[i][j].removed_domain:
                        neg_candids += 1
                elif self.csp.data[i][j] == 'r' or self.csp.data[i][j] == 'd':
                    if -1 not in self.csp.mp[i][j].removed_domain:
                        plus_candids += 1
                    if 1 not in self.csp.mp[i][j].removed_domain:
                        neg_candids += 1
            if plus_sum > self.csp.row_vals[i]:
                return 'failure'
            if neg_sum > self.csp.row_nvals[i]:
                return 'failure'
            if self.csp.row_vals[i] - plus_sum > plus_candids:
                return 'failure'
            if self.csp.row_nvals[i] - neg_sum > neg_candids:
                return 'failure'
            exact_plus = self.csp.row_vals[i] - plus_sum == plus_candids
            exact_neg = self.csp.row_nvals[i] - neg_sum == neg_candids
            if exact_plus or exact_neg:
                for j in range(0, self.csp.cols):
                    if self.csp.data[i][j] == 'l' or self.csp.data[i][j] == 'u':
                        if exact_plus and 1 not in self.csp.mp[i][j].removed_domain:
                            if not self.csp.mp[i][j].same_row() and -1 not in self.csp.mp[i][j].removed_domain:
                                 inferences.append(Inference(self.csp.mp[i][j], -1))
                            if 0 not in self.csp.mp[i][j].removed_domain:
                                inferences.append(Inference(self.csp.mp[i][j], 0))
                        if exact_neg and -1 not in self.csp.mp[i][j].removed_domain:
                            if not self.csp.mp[i][j].same_row() and 1 not in self.csp.mp[i][j].removed_domain:
                                inferences.append(Inference(self.csp.mp[i][j], 1))
                            if 0 not in self.csp.mp[i][j].removed_domain:
                                inferences.append(Inference(self.csp.mp[i][j], 0))
                    elif self.csp.data[i][j] == 'r' or self.csp.data[i][j] == 'd':
                        if exact_plus and -1 not in self.csp.mp[i][j].removed_domain:
                            if not self.csp.mp[i][j].same_row() and 1 not in self.csp.mp[i][j].removed_domain:
                                inferences.append(Inference(self.csp.mp[i][j], 1))
                            if 0 not in self.csp.mp[i][j].removed_domain:
                                inferences.append(Inference(self.csp.mp[i][j], 0))
                        if exact_neg and 1 not in self.csp.mp[i][j].removed_domain:
                            if not self.csp.mp[i][j].same_row() and -1 not in self.csp.mp[i][j].removed_domain:
                                inferences.append(Inference(self.csp.mp[i][j], -1))
                            if 0 not in self.csp.mp[i][j].removed_domain:
                                inferences.append(Inference(self.csp.mp[i][j], 0))

        #Like before, just do it for columns
        for j in self.cols:
            plus_sum = 0
            neg_sum = 0
            plus_candids = 0
            neg_candids = 0
            for i in range(0, self.csp.rows):
                if self.csp.data[i][j] == '+':
                    plus_sum += 1
                elif self.csp.data[i][j] == '-':
                    neg_sum += 1
                elif self.csp.data[i][j] == 'l' or self.csp.data[i][j] == 'u':
                    if 1 not in self.csp.mp[i][j].removed_domain:
                        plus_candids += 1
                    if -1 not in self.csp.mp[i][j].removed_domain:
                        neg_candids += 1
                elif self.csp.data[i][j] == 'r' or self.csp.data[i][j] == 'd':
                    if -1 not in self.csp.mp[i][j].removed_domain:
                        plus_candids += 1
                    if 1 not in self.csp.mp[i][j].removed_domain:
                        neg_candids += 1
            if plus_sum > self.csp.col_vals[j]:
                return 'failure'
            if neg_sum > self.csp.col_nvals[j]:
                return 'failure'
            if self.csp.col_vals[j] - plus_sum > plus_candids:
                return 'failure'
            if self.csp.col_nvals[j] - neg_sum > neg_candids:
                return 'failure'
            exact_plus = self.csp.col_vals[j] - plus_sum == plus_candids
            exact_neg = self.csp.col_nvals[j] - neg_sum == neg_candids
            if exact_plus or exact_neg:
                for i in range(0, self.csp.rows):
                    if self.csp.data[i][j] == 'l' or self.csp.data[i][j] == 'u':
                        if exact_plus and 1 not in self.csp.mp[i][j].removed_domain:
                            if not self.csp.mp[i][j].same_col() and -1 not in self.csp.mp[i][j].removed_domain:
                                 inferences.append(Inference(self.csp.mp[i][j], -1))
                            if 0 not in self.csp.mp[i][j].removed_domain:
                                inferences.append(Inference(self.csp.mp[i][j], 0))
                        if exact_neg and -1 not in self.csp.mp[i][j].removed_domain:
                            if not self.csp.mp[i][j].same_col() and 1 not in self.csp.mp[i][j].removed_domain:
                                inferences.append(Inference(self.csp.mp[i][j], 1))
                            if 0 not in self.csp.mp[i][j].removed_domain:
                                inferences.append(Inference(self.csp.mp[i][j], 0))
                    elif self.csp.data[i][j] == 'r' or self.csp.data[i][j] == 'd':
                        if exact_plus and -1 not in self.csp.mp[i][j].removed_domain:
                            if not self.csp.mp[i][j].same_col() and 1 not in self.csp.mp[i][j].removed_domain:
                                inferences.append(Inference(self.csp.mp[i][j], 1))
                            if 0 not in self.csp.mp[i][j].removed_domain:
                                inferences.append(Inference(self.csp.mp[i][j], 0))
                        if exact_neg and 1 not in self.csp.mp[i][j].removed_domain:
                            if not self.csp.mp[i][j].same_col() and -1 not in self.csp.mp[i][j].removed_domain:
                                inferences.append(Inference(self.csp.mp[i][j], -1))
                            if 0 not in self.csp.mp[i][j].removed_domain:
                                inferences.append(Inference(self.csp.mp[i][j], 0))

        return inferences
