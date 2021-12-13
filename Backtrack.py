from Assignment import Assignment
from Csp import Csp
from Var import Var


class BackTrack():
    csp = None
    
    
    def __init__(self, csp: Csp):
        self.csp = csp

    #Returns a solution or failure
    def search(self):
        return self.backtrack(Assignment(self.csp.rows, self.csp.cols))

    #Returns a solution or failure
    def backtrack(self, assignment: Assignment):
        if self.complete(assignment):
            return assignment

        var = self.select_unassigned_variable(assignment, self.csp)
        # if var is not None:
            # print('r: %d c: %d, modes: %d\n' % (var.r, var.c, len(self.order_domain_values(var, assignment))))
        for value in self.order_domain_values(var, assignment):
            if self.consistent(var, value, assignment):
                assignment.append(var, value)
                inferences = self.inference(var,value, assignment)
                if inferences != 'failure':
                    assignment.append(inferences)
                result = self.backtrack(assignment)
                if result != 'failure':
                    return result
                assignment.remove(var)
                #assignment.remove(inferences)
        return 'failure'

    def select_unassigned_variable(self, assignment: Assignment, csp):
        unassigned = list(filter(lambda x : x.value == -100 ,assignment.variables))
        if len(unassigned) == 0:
            return None
        min = unassigned[0]

        for var in unassigned:
            if var == min:
                continue
            r = len(assignment.remaining_possible_values(var))
            n = len(assignment.remaining_possible_values(min))

            if r < n:
                min = var
            #else if r= n

        return min
                
    def complete(self, assignment: Assignment):
        #Check the first row, get sum of +, sum of -, check rules, so on...
        for i in range(0, self.csp.rows):
            plus_sum = 0
            neg_sum = 0
            for j in range(0, self.csp.cols):
                if assignment.is_positive(i,j):
                    plus_sum += 1
                if assignment.is_negative(i,j):
                    neg_sum += 1
            if plus_sum != self.csp.row_vals[i]:
                return False
            if neg_sum != self.csp.row_nvals[i]:
                return False

        #Like before, just do it for columns
        for j in range(0, self.csp.cols):
            plus_sum = 0
            neg_sum = 0
            for i in range(0, self.csp.rows):
                if assignment.is_positive(i,j):
                    plus_sum += 1
                if assignment.is_negative(i,j):
                    neg_sum += 1
            if plus_sum != self.csp.col_vals[j]:
                return False
            if neg_sum != self.csp.col_nvals[j]:
                return False

        return True

    def order_domain_values(self, var: Var, assignment: Assignment):
        if var is None:
            return []
        return [0,1,-1]

    def consistent(self, var, value, assignment: Assignment):
        l = len(assignment.remaining_possible_values(var))
        if l == 3:
            return True
        return False

    # def inference(var, value, assignment):
        # It blocks some
        # It stops some from being same charge
