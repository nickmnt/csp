from Assignment import Assignment
from Csp import Csp
from Var import Var


class BackTrack():
    csp = None
    
    
    def __init__(self, csp: Csp):
        self.csp = csp

    #Returns a solution or failure
    def search(self):
        return self.backtrack([])

    #Returns a solution or failure
    def backtrack(self, assignment: list):
        if self.complete(assignment):
            return assignment

        var = self.select_unassigned_variable()
        for value in self.order_domain_values(var, assignment):
            if self.consistent(value, assignment):
                assignment.append(value)
            inferences = self.inference(var,value)
            if inferences != 'failure':
                assignment.append(inferences)
                result = self.backtrack(assignment)
                if result != 'failure':
                    return result
            assignment.remove(value)
            assignment.remove(inferences)
        return 'failure'

    def select_unassigned_variable(self, assignment: Assignment, csp):
        unassigned = filter(lambda x : x.value != -100 ,assignment.variables)
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
                
    def complete(self, assignment):
        #Check the first row, get sum of +, sum of -, check rules, so on...
        for i in range(0, self.rows):
            plus_sum = 0
            neg_sum = 0
            for j in range(0, self.cols):
                if assignment.data[i][j] == 1:
                    plus_sum += 1
                if assignment.data[i][j] == -1:
                    neg_sum += 1
            if plus_sum != self.row_vals[i]:
                return False
            if neg_sum != self.row_nvals[i]:
                return False

        #Like before, just do it for columns
        for i in range(0, self.cols):
            plus_sum = 0
            neg_sum = 0
            for j in range(0, self.rows):
                if assignment.data[j][i] == 1:
                    plus_sum += 1
                if assignment.data[j][i] == -1:
                    neg_sum += 1
            if plus_sum != self.col_vals[i]:
                return False
            if neg_sum != self.col_nvals[i]:
                return False

        return True
