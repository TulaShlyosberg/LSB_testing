from PIL import Image
import numpy as np
import os


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
