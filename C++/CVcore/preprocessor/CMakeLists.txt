cmake_minimum_required(VERSION 3.12)
project(preprocessor)

# Установите политику для устранения предупреждения
if(POLICY CMP0148)
    cmake_policy(SET CMP0148 NEW)
endif()

set(CMAKE_CXX_STANDARD 20)

# Используйте современный FindPython вместо устаревшего FindPythonLibs
set(PYBIND11_FINDPYTHON ON)

# Явное указание путей Python
set(PYTHON_INCLUDE_DIR "C:/msys64/mingw64/include/python3.12")
set(PYTHON_LIBRARY "C:/msys64/mingw64/lib/libpython3.12.dll.a")

find_package(OpenCV REQUIRED COMPONENTS core)
find_package(pybind11 REQUIRED)

include_directories(
        ${PYTHON_INCLUDE_DIR}
        ${OpenCV_INCLUDE_DIRS}
        C:/msys64/mingw64/include/opencv4
)

add_executable(preprocessor main.cpp)

target_link_libraries(preprocessor
        ${OpenCV_LIBS}
        ${PYTHON_LIBRARY}
)

message(STATUS "Using Python from: ${PYTHON_INCLUDE_DIR}")
message(STATUS "OpenCV libraries: ${OpenCV_LIBS}")