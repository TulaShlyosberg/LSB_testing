def neighbors(matrix, i, j):
    # Count alive neighbours for cell [i][j]
    summ = 0
    if i > 0:
        summ += matrix[i - 1][j]
        if j > 0:
            summ += matrix[i - 1][j - 1]
        if j + 1 < len(matrix[i]):
            summ += matrix[i - 1][j + 1]
    if j > 0:
        summ += matrix[i][j - 1]
    if j + 1 < len(matrix[i]):
        summ += matrix[i][j + 1]
    if i + 1 < len(matrix):
        summ += matrix[i + 1][j]
        if j > 0:
            summ += matrix[i + 1][j - 1]
        if j + 1 < len(matrix[i]):
            summ += matrix[i + 1][j + 1]
    return summ


def iter(matrix):
    # Count next state of matrix
    cnt = [[0] * len(matrix[_]) for _ in range(len(matrix))]
    for i1 in range(len(matrix)):
        for j1 in range(len(matrix[i1])):
            cnt[i1][j1] = neighbors(matrix, i1, j1)

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if cnt[i][j] == 3:
                matrix[i][j] = 1
            elif cnt[i][j] == 2 and matrix[i][j] == 1:
                continue
            else:
                matrix[i][j] = 0

    return matrix


def living(matrix, days=1):
    # Imitate 'days' days of matrix's life
    for _ in range(days):
        matrix = iter(matrix)

    return matrix


def read():
    # a file, where is matrix for game
    fin = open("matrix.txt", "r")

    # high and width of matrix
    n, m = list(map(int, input().split()))

    # for file like "010"
    # matrix = [[int(elem) for elem in list(fin.readline().rstrip())] for q in range(n)]

    # for file like "0 1 0"
    matrix = [list(map(int, fin.readline().rstrip().split())) for _ in range(n)]

    # for stdin
    # matrix = [list(map(int, input().split())) for q in range(n)]

    return matrix


def write(matrix):
    # print a state of matrix after 'days' days (iterations)
    fout = open("matrix.txt", "w")
    for line in matrix:
        print(*line, file=fout)
