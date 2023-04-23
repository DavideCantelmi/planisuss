def createMatrix (n, m):
    map = list[n][m]
    return map

def populateMatrix(map, livingBeing, x, y):
    if (isinstance(livingBeing, "Erbast")):
        map[x][y] = 'G'
    elif (isinstance(livingBeing, "Carviz")):
        map[x][y] = 'R'
    elif (isinstance(livingBeing, "Vegetob")):
        map[x][y] = 'B'




