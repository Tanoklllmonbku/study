#include <iostream>
#include <opencv2/core.hpp>
#include <pybind11/numpy.h>

int main() {
    std::cout << "Testing OpenCV basic functionality..." << std::endl;

    // Простая проверка без сложных операций
    cv::Mat mat(2, 2, CV_8UC1);
    mat.setTo(5);

    std::cout << "Matrix created successfully" << std::endl;
    std::cout << "OpenCV version: " << CV_VERSION << std::endl;
    std::cout << "Test passed!" << std::endl;
    std::cout << "Python!!!"<<std::endl;

    return 0;
}