from Backtrack import BackTrack
from Csp import Csp
from Var import Var


if __name__ == "__main__":
    nums = [int(x) for x in input().split()]
    
    rows = int(nums[0])
    cols = int(nums[1])

    row_vals = [0] * rows
    row_nvals = [0] * rows
    col_vals = [0] * cols
    col_nvals = [0] * cols

    nums = [int(x) for x in input().split()]
    for i in range(0, rows):
        row_vals[i] = int(nums[i])
    nums = [int(x) for x in input().split()]
    for i in range(0, rows):
        row_nvals[i] = int(nums[i])
    nums = [int(x) for x in input().split()]
    for i in range(0, cols):
        col_vals[i] = int(nums[i])
    nums = [int(x) for x in input().split()]
    for i in range(0, cols):
        col_nvals[i] = int(nums[i])

    data = [[0 for i in range(cols)] for j in range(rows)]
    mp = [[[] for i in range(cols)] for j in range(rows)]
    variables = []
    for i in range(rows):
        nums = [int(x) for x in input().split()]
        for j in range(cols):
            if nums[j] == 0:
                if j-1 >= 0 and nums[j-1] == '0':
                    data[i][j] = 'r'
                    var = Var(i, j-1, 0)
                    mp[i][j-1].append(var)
                    mp[i][j].append(var)
                    variables.append(var)
                else:
                    data[i][j] = 'l'
            elif nums[j] == 1:
                if i-1 >= 0 and data[i-1][j] == '1':
                    data[i][j] = 'd'
                    var = Var(i, j, 1)
                    mp[i-1][j].append(var)
                    mp[i][j].append(var)
                    variables.append(var)
                else:
                    data[i][j] = 'u'
            else:
                data[i][j] = 'x'

    csp = Csp(rows, cols, row_vals, col_vals, row_nvals, col_nvals, data, mp, variables)
    backtrack = BackTrack(csp)
    print(backtrack.search())

