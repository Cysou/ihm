class Astar:

    def __init__(self):
        self.matrix = None
        self.N = None
        self.M = None
        self.start = None
        self.end = None
        self.finish = None

    def search(self, matrix, wall, start, end):
        """initialise les variables
        et lance la fonction récurrente"""
        self.matrix = matrix
        self.N = len(matrix)
        self.M = len(matrix[0])
        self.start = self.get_index(start)
        self.end = self.get_index(end)
        self.wall = wall
        return self.pathfinder()

    def pathfinder(self):
        """ """
        queue = [self.start]
        new_queue = []
        visited = [self.start]
        while len(queue) > 0:
            for current in queue:
                current = queue[-1]
                if current == self.end:
                    return True

                for index in self.get_neighbors(current):
                    if self.matrix[index[0]][index[1]] != self.wall:
                        if index not in visited:
                            new_queue.append(index)
                            visited.append(index)

            queue = new_queue
            new_queue = []
        return False


    def get_index(self, num):
        for i in range(self.N):
            for j in range(self.M):
                if self.matrix[i][j] == num:
                    return (i, j)

    def get_neighbors(self, index):
        i = index[0]
        j = index[1]
        neighbors = []
        for i, j in [(i, j-1), (i-1, j), (i, j+1), (i+1, j)]:
            if 0 < i < self.N and 0 < j < self.M:
                neighbors.append((i, j))
        return neighbors

def create_matrix(file_name):
    with open(file_name, "r") as fd:
        matrix = []
        i = 0
        for line in fd:
            line = line.strip()
            line = line.split(" ")
            for i in range(len(line)):
                line[i] = int(line[i])
            print(line)
            matrix.append(line)
    return matrix

if __name__ == '__main__':

    matrix = create_matrix("map/custom/test.map")

    astar = Astar()
    b = astar.search(matrix, 1, 2, 3)
    print(b)
