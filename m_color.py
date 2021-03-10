class graph():
    def __init__(self):
        self.V=4
        self.fin_col=[0,0,0,0]
        #self.graph=[[0 for column in range]]
    def graphcoloring(self,map,maxcolors):
        V=self.V
        for i in range(V):
            for color in range(1,maxcolors+1):
                if self.issafe(map,i,color):
                    self.assigncolor(i,color)
                    break
                else:
                    if color>=maxcolors:
                        print("Not possible")
                        return 
                    else:
                        continue
        print(self.fin_col)

    def issafe(self,map,v,color):
        for i in range(self.V):
            if map[v][i]==1 and self.fin_col[i]==color:
                return False
        return True
    def assigncolor(self,vertex,color):
        #self.fin_col.append(color) 
        self.fin_col[vertex]=color       
if __name__=="__main__":
    map=[[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1],[1,1,1,1]]
    maxcolors=3
    g=graph()
    g.graphcoloring(map,maxcolors)