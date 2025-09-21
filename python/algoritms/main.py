from sorting.algoritms import BubbleSort
from sorting.base import return_algoritm

def main(name:str, data:list):
    algorithm = return_algoritm(name, data)
    return algorithm

if __name__ == '__main__':
    name = input("Insert algorithm name: \n")
    data = input("Insert data set (Comma separating, without spaces): \n").split(',')
    print(main(name, data))
