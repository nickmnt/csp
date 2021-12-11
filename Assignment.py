from Var import Var


class Assignment(): 
    rows = -1
    cols = -1
    variables = []
    horz = []
    vert = []
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

    def append(self, val: Var):
        if val.type == 0:
            self.horz[val.r][val.c] = val.value
        elif val.type == 1:
            self.vert[val.r][val.c] = val.value

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
                return False
        
        #self vert 
        if self.check_r_range(r):
            val = self.vert[r][c].value
            if val == 1:
                return False

        #If upper vert exists
        if self.check_r_range(r-1):
            val = self.vert[r-1][c].value
            if val == -1:
                return False
        #If left horz exists
        if self.check_c_range(c-1) >= 0:
            val = self.horz[r][c-1].value
            if val == -1:
                return False

    def is_negative(self, r, c):
        #self horz
        if self.check_c_range(c):
            val = self.horz[r][c].value
            if val == -1:
                return False
        
        #self vert 
        if self.check_r_range(r):
            val = self.vert[r][c].value
            if val == -1:
                return False

        #If upper vert exists
        if self.check_r_range(r-1):
            val = self.vert[r-1][c].value
            if val == 1:
                return False
        #If left horz exists
        if self.check_c_range(c-1) >= 0:
            val = self.horz[r][c-1].value
            if val == 1:
                return False