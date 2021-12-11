from Backtrack import BackTrack
from Csp import Csp


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

    csp = Csp(rows, cols, row_vals, col_vals, row_nvals, col_nvals)
    backtrack = BackTrack(csp)
    print(backtrack.search())

