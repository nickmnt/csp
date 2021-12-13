class Var(): 
    r = -1
    c = -1
    # 0 - _
    # 1 - |
    type = -1
    value = -100
    domain = [0,1,-1]
    removed_domain = []

    def __init__(self,r,c,type):
        self.r = r
        self.c = c
        self.type = type