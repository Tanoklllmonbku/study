#include <iostream>
#include <utility>

void ArrayReverse(int size, int array[]) {
    for (int i = 0; i < size / 2; ++i) {
        std::swap(array[i], array[size - i - 1]);
    }
}

void ArrayRead(int size, const int array[]) {

    for (int i = 0; i < size-1; ++i) {

        std::cout << array[i] << ", ";
    }
    std::cout << array[size-1] << ".\n";
}

int main() {
    const int ARRAY_SIZE = 5;
    int arr[ARRAY_SIZE] = {1, 2, 3, 4, 5};
    std::cout << "Array: \n" ;
    ArrayRead(ARRAY_SIZE, arr);
    std::cout << "Array length: ";
    std::cout << ARRAY_SIZE << "\n";
    std::cout << "Reversed array: \n";
    ArrayReverse(ARRAY_SIZE, arr);
    ArrayRead(ARRAY_SIZE, arr);
    std::cout << "Press any key for continue...";
    std::cin.get();

    return 0;
}

