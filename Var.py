class Var(): 
    r = -1
    c = -1
    # 0 - _
    # 1 - |
    type = -1
    value = 0

    def __init__(self,r,c,type):
        self.r = r
        self.c = c
        self.type = type