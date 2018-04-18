from PIL import Image
import numpy as np
import os
from collections import defaultdict
from collections import deque
import matplotlib.pyplot as plt


#Создает файл - результат фильтрации последнего бита в байте 
def pictures_lsb(path, name, ind):
    container = Image.open(os.path.join(path, name))
    im_size = container.size
    im_str = container.tobytes()
    result = [255*(j % 2**(ind + 1) // 2**ind) for j in im_str]
    ans = container.frombytes(bytes(result), 'raw')
    container.save(os.path.join(path, 'filtered', 'r_' + name), 
                   container.format)


#Считывает из файла в матрицу из 1 и 0
def lsb_to_matrix(path, name):
    container = Image.open(os.path.join(path, name))
    im_str = container.tobytes()
    result = np.array([j//255 for j in im_str])
    result = np.resize(result, (container.size[0]*len(container.mode),
                               container.size[1]))
    return result


#Каждому байту сопоставляет бит на месте ind
def picture_to_lsb_matrix(path, name, ind):
    container = Image.open(os.path.join(path, name))
    im_size = container.size
    im_str = container.tobytes()
    result = np.array([j % 2**(ind + 1) // 2**ind for j in im_str])
    result = np.resize(result, (container.size[0]*len(container.mode), container.size[1]))
    return result

def matrix_to_picture(matrix, size, path, name):
    container = Image.new('RGBA', size)
    container.frombytes(bytes(matrix), 'raw')
    container.save(os.path.join(path, name), 'png')

def shenon_entropy(matrix):
    probabilties = [0.0] * matrix.shape[0]
    for i in matrix:
        probabilties[np.bincount(i)[0]] += 1
    probabilties = [j / sum(probabilties) if j > 0 else 1 for j in probabilties]
    H = 0 - np.sum(np.array(probabilties) * np.log2(probabilties))
    return H

def dfs(i, j, matrix, visited):
    stack = deque()
    stack.append((i, j))
    res = 1
    while len(stack) > 0:
        i, j = stack.pop()
        visited.add((i, j))
        if i > 0 and (i-1, j) not in visited and matrix[i-1][j] == 0:
            res += 1
            stack.append((i-1, j))
        if i < len(matrix) - 1 and (i + 1, j) not in visited and matrix[i+1][j] == 0:
            res += 1
            stack.append((i + 1, j))
        if j > 0 and (i, j - 1) not in visited and matrix[i][j-1] == 0:
            res += 1
            stack.append((i, j - 1))
        if j < len(matrix[0]) - 1 and (i, j + 1) not in visited and matrix[i][j + 1] == 0:
            res += 1
            stack.append((i, j + 1))
    return res


def black_area_frequencies(matrix, left, right):
    width = len(matrix[0])
    height = len(matrix)
    length = right - left
    frequencies = [0]*length
    visited = set()
    for i in range(height):
        for j in range(width):
            if (i, j) not in visited and matrix[i][j] == 0:
                ans = dfs(i, j, matrix, visited)
                if ans >= left and ans < right:
                    frequencies[ans - left] += 1
    return frequencies

def get_balck_area_graphics(path, name_from, name_to, left, right):
    matr = sf.picture_to_lsb_matrix(path, 'name_from', 0)
    frequencies = sf.black_area_frequencies(matr, left, right)
    fig = plt.figure()
    plt.title('Распределение черных областей по рисунку')
    plt.plot(range(left, right), frequencies)
    plt.savefig(os.path.join(path, name_to))