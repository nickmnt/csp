class Csp():
    rows = -1
    cols = -1
    row_vals = None
    col_vals = None
    row_nvals = None
    col_nvals = None
    data = None
    map = None
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