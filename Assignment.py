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


        max, min = (-1,-1)
        if rows >= cols:
            max = rows
        else:
            max = cols

        self.horz = [[0 for i in range(cols-1)] for j in range(rows)]
        self.horz = [[0 for i in range(cols)] for j in range(rows-1)]
        # -
        for i in range(0, rows):
            for j in range(0, cols-1):
                var = Var(i,j, 0)
                self.horz[i][j] = var
                self.variables.append(var)
        # |
        for j in range(0, cols):
            for i in range(0, rows-1):
                var = Var(i,j, 0)
                self.vert[i][j] = var
                self.variables.append(var)

    def append(self, val: Var):
        if val.type == 0:
            self.horz[val.r][val.c] = val.value
        elif val.type == 1:
            self.vert[val.r][val.c] = val.value

    def delete_action(self, val: Var):
        if val.type == 0:
            self.horz[val.r][val.c] = 0
        elif val.type == 1:
            self.vert[val.r][val.c] = 0
            
        