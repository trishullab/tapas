class Solution:
    def shortestBridge(self, A: List[List[int]]) -> int:
        """"
        1. find the 1st island (DFS)
        2. increment on the 1st island's boundary until it hit island (BFS)
        3. return the step
        """
        def dfs(i, j):
            A[i][j] = -1  # mark as visited
            queue.append((i, j))
            for x, y in ((i-1, j), (i+1, j), (i, j-1), (i, j+1)):
                if 0 <= x < n and 0 <= y < n and A[x][y] == 1:
                    dfs(x, y)
        
        def first():
            for i in range(len(A)):
                for j in range(len(A[0])):
                    if A[i][j] == 1:
                        return (i, j)
        
        # step 1 find the 1st island
        queue = deque()
        n = len(A)
        dfs(*first())
        
        # step 2 BFS from island 1
        step = 0 # because we start from island 1
        while queue:
            size = len(queue)
            for _ in range(size):
                i, j = queue.popleft()
                A[i][j] = -1
                for x, y in ((i-1, j), (i+1, j), (i, j-1), (i, j+1)):
                     if 0 <= x < n and 0 <= y < n:
                        if A[x][y] == 1:
                            return step
                        elif A[x][y] == 0: 
                            A[x][y] = -1  #  關鍵 才不會把重複的add to queue, will TLE if not
                            queue.append((x, y))      
            step += 1
        return 0