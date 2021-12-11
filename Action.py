class Action():
    r = -1
    c = -1
    direction = ''
    
    def __init__(self, r, c, direction):
        if (direction != 'R'
        and direction != 'L'
        and direction != 'U'
        and direction != 'D'):
            raise ValueError("Direction must be either 'R','L','U','D'")
        
        if (r < 0 or c < 0):
            raise ValueError("X and Y must be greater than or equal 0")

        #We must also check for the second block being in the range, etc, but this is a simple check

        self.r = r
        self.c = c
        self.direction = direction


    @staticmethod
    def is_valid(r, c, rows, cols):
        if r < 0 or c < 0 or r >= rows or c >= cols:
            return False
        return True

    
    @staticmethod
    def is_valid(r, c, direction, rows, cols):
        if not Action.is_valid(r,c,rows,cols):
            return False

        if direction == 'R':
            if not Action.is_valid(r,c+1, rows, cols):
                return False
        elif direction == 'L':
            if not Action.is_valid(r,c-1, rows, cols):
                return False
        elif direction == 'D':
            if not Action.is_valid(r+1,c, rows, cols):
                return False
        elif direction == 'U':
            if not Action.is_valid(r-1,c, rows, cols):
                return False
        return True