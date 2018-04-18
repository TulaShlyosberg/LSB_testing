import sten_func as sf
import os
import numpy


def main():
    path = os.path.join(os.getcwd(), 'images')
    matrix = sf.picture_to_lsb_matrix(path, 'china.png', 2)
    print(sf.shenon_entropy(matrix))
    matrix = sf.picture_to_lsb_matrix(path, 'china_stego.png', 2)
    print(sf.shenon_entropy(matrix))


if __name__ == '__main__':
    main()
