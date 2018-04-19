import sten_func as sf
import os
import numpy
import matplotlib.pyplot as plt
import compression as cmpr

def test_chi_square():
    '''
    
    '''
    path = os.path.join(os.getcwd(), 'images')
    print(sf.chi_square(path, 'sinica.png', 0, 0, 100, 10, 0))
    path = os.path.join(os.getcwd(), 'images\encoded')
    print(sf.chi_square(path, 'enc_sinica.png', 0, 0, 100, 10, 0))
    return

def main():
    test_1()
    
def test_3():
    left = 5
    right = 100    
    sf.encode(path, 'sinica.png', 'data.txt')
    matrix_1 = sf.picture_to_lsb_matrix_colored(path, 'sinica.png', 0, 0)
    matrix_2 = sf.picture_to_lsb_matrix_colored(path + '\\encoded', 'enc_sinica.png', 0, 0)
    freq_1 = sf.black_area_frequencies(matrix_1[0:200, 0:200], left, right)
    freq_1 = sorted(freq_1, reverse=True)
    freq_2 = sf.black_area_frequencies(matrix_2[0:200, 0:200], left, right)
    freq_2 = sorted(freq_2, reverse=True)
    print('E_wout_st = {}'.format(sum([i*freq_1[i] for i in range(len(freq_1))]) / sum(freq_1) / 40000))
    print('E_w_st = {}'.format(sum([i*freq_2[i] for i in range(len(freq_2))]) / sum(freq_2) / 40000))
    fig = plt.figure()
    plt.title('Рапределение черных полей')
    plt.plot(range(left, right), freq_1, label = 'Without_stego')
    plt.plot(range(left, right), freq_2, label = 'With_stego')
    plt.legend()
    plt.savefig(os.path.join(path, 'result.png'))

if __name__ == '__main__':
    main()
