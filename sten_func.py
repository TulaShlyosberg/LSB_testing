from PIL import Image
import numpy as np
import os
from collections import deque
import matplotlib.pyplot as plt
import stego_encoded as ste
import life


# Создает файл - результат фильтрации последнего бита в байте
def pictures_lsb(path, name, ind=0):
    '''
    Создает файл - результат фильтрации последнего бита в байте
    :param path:
    :param name:
    :param ind:
    :return:
    '''

    container = Image.open(os.path.join(path, name))
    im_size = container.size
    im_str = container.tobytes()
    result = [255*(j % 2**(ind + 1) // 2**ind) for j in im_str]
    ans = container.frombytes(bytes(result), 'raw')
    container.save(os.path.join(path, 'filtered', 'r_' + name), 
                   container.format)


def lsb_to_matrix(path, name):
    '''
    Делает из отфильтрованного файла матрицу
    '''
    container = Image.open(os.path.join(path, name))
    im_str = container.tobytes()
    result = np.array([j//255 for j in im_str])
    cod = len(container.mode)
    result = np.resize(result, (container.size[0]*cod,
                               container.size[1]))
    return result, cod


def picture_to_lsb_matrix(path, name, ind=0):
    '''
    Делает из картинки булевскую матрицу, вылеляя из каждого байта 
    '''
    container = Image.open(os.path.join(path, name))
    im_size = container.size
    im_str = container.tobytes()
    result = np.array([j % 2**(ind + 1) // 2**ind for j in im_str])
    cod = len(container.mode)
    result = np.resize(result, (container.size[0]*cod, container.size[1]))
    return result, cod


def picture_to_lsb_matrix_colored(path, name, ind, color):
    container = Image.open(os.path.join(path, name))
    im_size = container.size
    im_str = container.tobytes()
    cod = len(container.mode)
    result = np.array([im_str[j] % 2**(ind + 1) // 2**ind for j in range(color, len(im_str), cod)])
    result = np.resize(result, (container.size[0], container.size[1]))
    return result


def matrix_to_picture(matrix, size, path, name):
    container = Image.new('RGBA', size)
    container.frombytes(bytes(matrix), 'raw')
    container.save(os.path.join(path, name), 'png')


def shenon_entropy(matrix):
    probabilties = [0.0] * (matrix.shape[0] + 1)
    for i in matrix:
        if 0 in i:
            probabilties[np.bincount(i)[0]] += 1
        else:
            probabilties[0] += 1
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


def chi_square_from_frag(frag):
    frequencies_1 = np.zeros(128)
    frequencies_2 = np.zeros(128)
    if len(frag) == 0:
        return -1
    for i in frag:
        if i % 2 == 1:
            frequencies_1[i // 2] += 1
        if i % 2 == 0:
            frequencies_2[i//2] += 1
    delta = (frequencies_1 - frequencies_2)**2 / np.sum(frequencies_1 + frequencies_2)**2
    return np.sum(delta)


def chi_square(path, name, x, y, width, height, color):
    '''
    Хи-функция для фрагмента фотографии
    path - путь к дирректории, где лежит файл
    name - имя файла
    x, y - координаты верхнего левого угла фрагмента
    width - ширина фрагмента
    height - высота фрагмента
    color - номер цвета (R - 0, G - 1, B - 2, A - 3), в котором лежит стеганография
    '''
    container = Image.open(os.path.join(path, name))
    im_str = container.tobytes()
    cod = len(container.mode)
    frag = loupe(im_str, x, y, width, height, container.size, cod)
    return chi_square_from_frag(frag)


def chi_square_all(path, name, color):
    container = Image.open(os.path.join(path, name))
    height, width = container.size
    im_str = container.tobytes()
    cod = len(container.mode)
    for x in range(0, width, 100):
        for y in range(0, height, 100):
            frag = loupe(im_str, x, y, 100, 100, (height, width), cod)
            print('chi_square for coords({0}, {1}) is {2}'.format(x, y, chi_square_from_frag(frag)))


def black_area_frequencies(matrix, left, right):
    '''
    Функция возвращает массив frequenciesх[i from left to right] - количество встреч блоков площадью i 
    matrix - матрица, в которой ищем площади целиком заполненые нулями
    left - левая граница индекса
    right - правая граница индекса
    '''
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


def get_black_area_graphics(path, name_from, name_to, left, right):
    matr = picture_to_lsb_matrix(path, name_from, 0)
    frequencies = black_area_frequencies(matr, left, right)
    fig = plt.figure()
    plt.title('Распределение черных областей по lsb матрице рисунка')
    plt.plot(range(left, right), frequencies)
    plt.savefig(os.path.join(path, name_to))


def encode(path, name, frm):
    container = Image.open(os.path.join(path, name))
    im_str = container.tobytes()
    data = ste.extract_data(frm) + [0, 0]
    cod = len(container.mode)
    result = ste.write_data(data, im_str, cod)
    container.frombytes(bytes(result), 'raw')
    container.save(os.path.join(path, 'encoded\\enc_' + name), container.format)


def decode(path, name, out):
    container = Image.open(os.path.join(path, name))
    im_str = container.tobytes()
    cod = len(container.mode)
    result = ste.extract_message(im_str, cod)
    with open(out, "wb") as fout:
        fout.write(bytes(result))


def pictures_lsb_colored(path, name, ind, color):
    '''
    Фильтрует изображение, извлекая из каждого байта,
    соответсвующего цвету color, бит с номером ind,
    и формирует новое изображение
    :param path: путь до директории
    :param name: имя файла
    :param ind: номер бита
    :param color:
    :return:
    '''
    container = Image.open(os.path.join(path, name))
    im_size = container.size
    im_str = container.tobytes()
    if len(container.mode) == 4:
        result = [255*(im_str[j] % 2**(ind + 1) // 2**ind) if j % len(container.mode) == color 
                else 255 if j % len(container.mode) == 3 else 0 for j in range(len(im_str))]
    else:
        result = [255*(im_str[j] % 2**(ind + 1) // 2**ind) if j % len(container.mode) == color 
                  else 0 for j in range(len(im_str))]
    ans = container.frombytes(bytes(result), 'raw')
    container.save(os.path.join(path, 'filtered', 'r_' + name), 
                   container.format)


def loupe(im_str, x, y, width, height, size,  cod=1, color=0):
    result = list()
    p_width, p_height = size
    if x + width > p_width or y + height > p_height:
        return []
    for _y in range(y, y + height):
        for _x in range(x + color, x + width*cod + color, cod):
            result.append(im_str[_y*p_width*cod + _x])
    return result


def count_statistics(matrix, iterations):
    '''
    Считает энтропию Шеннона для нескольких итераций игры "Жизнь"
    :param matrix: матрица 0 и 1 для игры
    :param iterations: количество раундов игры
    :return: лист энтропий Шеннона, на i-м месте стоит энтропия для i-й итерации
    '''
    ans = [shenon_entropy(matrix)]
    for _ in range(iterations):
        matrix = life.living(matrix)
        ans.append(shenon_entropy(matrix))
    return ans
