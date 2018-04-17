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
