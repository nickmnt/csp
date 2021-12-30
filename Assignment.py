from Inference import Inference
from Var import Var

# THIS CLASS IS USELESS!!
# WAS IN PREVIOUS VERSIONS, REMOVED NOW!!!!
# USELESS!!
# USELESS!!
# USELESS!!
# USELESS!!
# USELESS!!
# USELESS!!
# USELESS!!
class Assignment(): 
    rows = -1
    cols = -1
    variables = []
    horz: "list[list[Var]]" = None
    vert: "list[list[Var]]" = None
    # row , col, direction: 'R', 'L', 'U', 'D'
    #last_action = (-1,-1,'')

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols

        self.horz = [[0 for i in range(cols-1)] for j in range(rows)]
        self.vert = [[0 for i in range(cols)] for j in range(rows-1)]
        # -
        for i in range(0, rows):
            for j in range(0, cols-1):
                var = Var(i,j, 0)
                self.horz[i][j] = var
                self.variables.append(var)
        # |
        for j in range(0, cols):
            for i in range(0, rows-1):
                var = Var(i,j, 1)
                self.vert[i][j] = var
                self.variables.append(var)

    def append(self, val: Var, value):
        if val.type == 0:
            self.horz[val.r][val.c].value = value
        elif val.type == 1:
            self.vert[val.r][val.c].value = value

    def remove(self, val: Var):
        if val.type == 0:
            self.horz[val.r][val.c].value = -100
        elif val.type == 1:
            self.vert[val.r][val.c].value = -100

    def check_r_range(self, r):
        return r < self.rows - 1 and r >= 0

    def check_c_range(self, c):
        return c < self.cols - 1 and c >= 0
            
    def check(self, r,c):
        #self horz
        if self.check_c_range(c):
            val = self.horz[r][c].value
            if val != -100 and val != 0:
                return False
        
        #self vert 
        if self.check_r_range(r):
            val = self.vert[r][c].value
            if val != -100 and val != 0:
                return False

        #If upper vert exists
        if self.check_r_range(r-1):
            val = self.vert[r-1][c].value
            if val != -100 and val != 0:
                return False
        #If left horz exists
        if self.check_c_range(c-1) >= 0:
            val = self.horz[r][c-1].value
            if val != -100 and val != 0:
                return False

        return True

    def remaining_possible_values(self, var: Var):
        return self.domain
        if not self.check(var.r,var.c):
            return [0]
        #horz
        if var.type == 0 and not self.check(var.r,var.c+1):
            return [0]
        #vert
        if var.type == 1 and not self.check(var.r+1,var.c):
            return [0]
        
        return [-1,0,1]

    def is_positive(self, r, c):
        #self horz
        if self.check_c_range(c):
            val = self.horz[r][c].value
            if val == 1:
                return True
        
        #self vert 
        if self.check_r_range(r):
            val = self.vert[r][c].value
            if val == 1:
                return True

        #If upper vert exists
        if self.check_r_range(r-1):
            val = self.vert[r-1][c].value
            if val == -1:
                return True
        #If left horz exists
        if self.check_c_range(c-1) >= 0:
            val = self.horz[r][c-1].value
            if val == -1:
                return True
        return False

    def is_negative(self, r, c):
        #self horz
        if self.check_c_range(c):
            val = self.horz[r][c].value
            if val == -1:
                return True
        
        #self vert 
        if self.check_r_range(r):
            val = self.vert[r][c].value
            if val == -1:
                return True

        #If upper vert exists
        if self.check_r_range(r-1):
            val = self.vert[r-1][c].value
            if val == 1:
                return True
        #If left horz exists
        if self.check_c_range(c-1) >= 0:
            val = self.horz[r][c-1].value
            if val == 1:
                return True
        return False

    def claim(self, r, c, inferences: list):
        #self horz
        if self.check_c_range(c):
            var = self.horz[r][c]
            if -1 not in var.removed_domain:
                inferences.append(Inference(var, -1))
            if 1 not in var.removed_domain:
                inferences.append(Inference(var, 1))
        #self vert 
        if self.check_r_range(r):
            var = self.vert[r][c]
            if -1 not in var.removed_domain:
                inferences.append(Inference(var, -1))
            if 1 not in var.removed_domain:
                inferences.append(Inference(var, 1))

        #If upper vert exists
        if self.check_r_range(r-1):
            var = self.vert[r-1][c]
            if -1 not in var.removed_domain:
                inferences.append(Inference(var, -1))
            if 1 not in var.removed_domain:
                inferences.append(Inference(var, 1))
        #If left horz exists
        if self.check_c_range(c-1) >= 0:
            var = self.horz[r][c-1]
            if -1 not in var.removed_domain:
                inferences.append(Inference(var, -1))
            if 1 not in var.removed_domain:
                inferences.append(Inference(var, 1))