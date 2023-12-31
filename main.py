import time
from parsing_methods import *
from show import show


def main():
    functions = all_func()
    to_json(functions)
    show(functions)


if __name__ == '__main__':
    print('=' * 69, 'Start process', '=' * 70)
    start_time = time.time()
    main()
    end_time = time.time()
    print(f'Program execution time: ', need_time := end_time - start_time, 'seconds.')
    print('=' * 69, 'Finish process', '=' * 70)
