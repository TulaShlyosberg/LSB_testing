import sten_func as sf
import os
import numpy
import matplotlib.pyplot as plt
import compression as cmpr


def test_black_square(name):
    left = 0
    right = 100
    height = 100
    width = 100
    path = os.path.join(os.getcwd(), 'images')
    matrix_1 = sf.picture_to_lsb_matrix_colored(path, name, 0, 0)
    matrix_2 = sf.picture_to_lsb_matrix_colored(path + '\\encoded', 'enc_{}.png'.format(name), 0, 0)
    freq_1 = sf.black_area_frequencies(matrix_1[0:width, 0:height], left, right)
    freq_2 = sf.black_area_frequencies(matrix_2[0:width, 0:height], left, right)
    try:
        print('E_wout_st = {}'.format(sf.black_area_excpection(freq_1, left, right)))
    except:
        print("There aren't black blocks with size between {} and {}, so E_wout_st = 0".format(left, right))
    try:
        print('E_w_st = {}'.format(sf.black_area_excpection(freq_2, left, right)))
    except:
        print("There aren't black blocks with size between {} and {}, so E_w_st = 0".format(left, right))
    fig = plt.figure()
    plt.title('Рапределение черных полей')
    plt.plot(range(left, right), freq_1, label = 'Without_stego')
    plt.plot(range(left, right), freq_2, label = 'With_stego')
    plt.legend()
    plt.savefig(os.path.join(path + '\\plots', name))


def test_life_iterations(name):
    path = os.path.join(os.getcwd(), 'images')
    matr_1 = sf.picture_to_lsb_matrix_colored(path, name, 0, 0)
    matr_2 = sf.picture_to_lsb_matrix_colored(path + '\\encoded', 'enc_' + name, 0, 0)
    ans_1 = sf.count_statistics(matr_1[0:200, 0:200], 10)
    ans_2 = sf.count_statistics(matr_2[0:200, 0:200], 10)
    fig = plt.figure()
    plt.title('Энтропия Шенона от итераций жизни')
    plt.plot(range(len(ans_1)), ans_1, label = 'Without stego')
    plt.plot(range(len(ans_2)), ans_2, label = 'With stego')
    plt.legend()
    plt.savefig(path + '\\plots\\life_' + name)



# Хи-квадрат для каждого элемента разбиения sinica.png и enc_sinica.png
def test_1():
    path = os.path.join(os.getcwd(), 'images')
    sf.chi_square_all(path, 'sinica.png', 0)
    path = os.path.join(os.getcwd(), 'images\encoded')
    sf.chi_square_all(path, 'enc_sinica.png', 0)
    return

# Шифрование в sinica.png - 30%
def test_2():
    path = os.path.join(os.getcwd(), 'images')
    sf.encode(path, 'sinica.png', 'data\\data_sinica.txt')

# Фильтр для enc_sinica.png
def test_3():
    path = os.path.join(os.getcwd(), 'images\encoded')
    sf.pictures_lsb_colored(path, 'enc_sinica.png', 0, 0)

# Декодирование из enc_sinica.png
def test_4():
    path = os.path.join(os.getcwd(), 'images\\encoded')
    sf.decode(path, 'enc_sinica.png', 'result.txt')

# Матожидание размера черного блока в углу 100x100 в sinica.png и enc_sinica.png
def test_5():
    test_black_square('sinica.png')

# Шифрование в mothers_kiss.png - 5%
def test_6():
    path = os.path.join(os.getcwd(), 'images')
    sf.encode(path, 'mothers_kiss.png', 'data\\data_mother.txt')
    return 

# Фильтр
def test_7():
    path = os.path.join(os.getcwd(), 'images\\encoded')
    sf.pictures_lsb_colored(path, 'enc_mothers_kiss.png', 0, 0)


# Хи-квадрат для стеганографии enc_mothers_kiss.png
def test_8():
    path = os.path.join(os.getcwd(), 'images\\encoded')
    sf.chi_square_all(path, 'enc_mothers_kiss.png', 0)
    return

# Мат. ожидание относительной площади черного блока в углу 100х100 в mothers_kiss.png и enc_mothers_kiss.png
def test_9():
    test_black_square('mother_kiss.png')


# Подсчет для угла 100х100 зависимости энтропии Шенона от итераций жизни
def test_10():
    test_life_iterations('mothers_kiss.png')


# Итерации жизни для sinica.png
def test_11():
    test_life_iterations('sinica.png')


# Кодирование в betchoven.png - 95%
def test_12():
    path = os.path.join(os.getcwd(), 'images')
    sf.encode(path, 'betchoven.png', 'data\\data_betchoven.txt')

# Зависимость энтропии Шенона от итераций жизни
def test_13():
    test_life_iterations('betchoven.png')

def test_14():
    path = os.path.join(os.getcwd(), 'images')
    sf.percentaged_encode(path, 'betchoven.png', 'data\\data_betchoven.txt', 30)
    path = os.path.join(os.getcwd(), 'images\\encoded')
    sf.pictures_lsb_colored(path, 'enc_betchoven.png', 0, 0)


def main():
    test_14()

if __name__ == '__main__':
    main()
