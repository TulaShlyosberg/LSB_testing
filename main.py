import sten_func as sf
import os


def main():
    path = os.path.join(os.getcwd(), 'images')
    sf.get_balck_area_graphics(path, 'Lena.png', 'Lena_graphic', 30, 200)


if __name__ == '__main__':
    main()
