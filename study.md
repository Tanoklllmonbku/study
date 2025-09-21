# THE ENGINEER’S MASTER ARCHITECTURE COURSE (EMAC)  
## ПОЛНАЯ ВЕРСИЯ  

### 3 года. 15 модулей. 60+ инструментов. 1 цель: стать Tech Lead в high-performance ML/industrial systems  

Философия:  
«Ты не учишь технологии. Ты решаешь реальные проблемы с их помощью. Каждый модуль — это операционная единица для решения конкретной задачи из твоей работы.»  

Формат:  
- Каждый модуль — автономный. Можно начать с любого.  
- Каждый модуль содержит: Проблема → Инструменты → Практика → Метрики → Документация → Продакшен-паттерны.  
- Каждый модуль заканчивается рабочим, деплоебельным, документированным продуктом.  
- Все модули связаны через GitPoster SDK (M13) — как единый пайплайн-движок.  

---

## M1: High-Performance CV Core — Сделай свою модель быстрее в 5x  

Проблема:  
Ваша OCR-модель обрабатывает один скан за 1.2 секунды. На линии — 10 камер, каждая по 30 кадров/минуту. Итого — 300 запросов/мин.  
Вы не можете масштабировать Python + OpenCV на CPU. Нужно <200 мс на изображение.  

Инструменты (выбираете только то, что нужно):  

| Инструмент | Роль | Почему именно он |
|----------|------|------------------|
| OpenCV C++ | Предобработка (resize, binarize, denoise) | В 8–10x быстрее Python. Не используйте cv2 из Python — он медленный. |
| pybind11 | Мост между C++ и Python | Позволяет вызывать C++-функцию как from cv_engine import preprocess |
| NumPy + Numba | Ускорение численных операций | Для простых операций (np.mean, np.clip) — JIT-компиляция даёт 2–4x |
| ONNX Runtime (C++) | Инференс модели | Легковесный, без GIL, поддерживает Intel MKL, TensorRT |
| Intel OpenVINO | Оптимизация на CPU | Если работаете на Intel Xeon/NUC — ускоряет в 2–3x |
| CUDA + cuDNN | GPU-ускорение | Если есть NVIDIA GPU — используйте torch.cuda или tensorrt |
| CMake + vcpkg | Сборка | Автоматизирует зависимость от OpenCV, ONNX, Boost |

Практика (поэтапно — 5 дней)

## День 1: Экспортируйте модель в ONNX

Шаги:
1. Установить torch:
```bash
python -m venv .venv
.venv/Scripts/activate
pip install torch torchvision torchaudio
```
2. Создать модель (Учебная):
```Python
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt

# Проверяем доступность GPU
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f'Using device: {device}')

# Параметры
batch_size = 64
learning_rate = 0.001
num_epochs = 5

# 1. Подготовка данных
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])

# Загрузка данных Fashion-MNIST
train_dataset = torchvision.datasets.FashionMNIST(
    root='./data',
    train=True,
    download=True,
    transform=transform
)

test_dataset = torchvision.datasets.FashionMNIST(
    root='./data',
    train=False,
    download=True,
    transform=transform
)

# Создаем DataLoader'ы
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

# Классы Fashion-MNIST
classes = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
           'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']


# 2. Визуализируем несколько изображений
def show_images():
    dataiter = iter(train_loader)
    images, labels = next(dataiter)

    fig, axes = plt.subplots(1, 5, figsize=(12, 3))
    for i in range(5):
        axes[i].imshow(images[i].squeeze(), cmap='gray')
        axes[i].set_title(classes[labels[i].item()])
        axes[i].axis('off')
    plt.show()


show_images()


# 3. Создаем модель нейронной сети
class NeuralNet(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super(NeuralNet, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, num_classes)

    def forward(self, x):
        x = x.reshape(-1, 28 * 28)  # Преобразуем изображение 28x28 в вектор 784
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        return x


# Инициализируем модель
input_size = 28 * 28  # Размер изображения Fashion-MNIST
hidden_size = 128
num_classes = 10

model = NeuralNet(input_size, hidden_size, num_classes).to(device)
print(model)

# 4. Определяем функцию потерь и оптимизатор
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=learning_rate)

# 5. Цикл обучения
total_step = len(train_loader)
for epoch in range(num_epochs):
    for i, (images, labels) in enumerate(train_loader):
        # Перемещаем данные на устройство (GPU/CPU)
        images = images.to(device)
        labels = labels.to(device)

        # Прямой проход
        outputs = model(images)
        loss = criterion(outputs, labels)

        # Обратный проход и оптимизация
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if (i + 1) % 100 == 0:
            print(f'Epoch [{epoch + 1}/{num_epochs}], Step [{i + 1}/{total_step}], Loss: {loss.item():.4f}')

print('Обучение завершено!')

# 6. Тестирование модели
model.eval()  # Переключаем модель в режим оценки
with torch.no_grad():  # Отключаем вычисление градиентов для ускорения
    correct = 0
    total = 0
    for images, labels in test_loader:
        images = images.to(device)
        labels = labels.to(device)
        outputs = model(images)
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

    print(f'Accuracy on test images: {100 * correct / total:.2f}%')

# 7. Сохранение модели
torch.save(model.state_dict(), 'fashion_mnist_model.pth')
print('Модель сохранена как fashion_mnist_model.pth')


# 8. Пример предсказания на одном изображении
def predict_example():
    model.eval()
    dataiter = iter(test_loader)
    images, labels = next(dataiter)

    # Берем первое изображение из батча
    image = images[0].unsqueeze(0).to(device)
    true_label = labels[0].item()

    # Делаем предсказание
    with torch.no_grad():
        output = model(image)
        _, predicted = torch.max(output, 1)
        predicted_label = predicted.item()

    # Визуализируем
    plt.imshow(images[0].squeeze(), cmap='gray')
    plt.title(f'True: {classes[true_label]}, Predicted: {classes[predicted_label]}')
    plt.axis('off')
    plt.show()


predict_example()
```
## День 2: Напишите C++-предобработку
Шаги:
1. Установка MSYS2:
```
https://www.msys2.org/
```
2. Команды MSYS2:
```
# На всё отвечать Y
# Обновление пакетов 
pacman -Syu
# Установка компилятора и инструментов
pacman -S --needed base-devel mingw-w64-x86_64-toolchain
# Установка CMake и других инструментов
pacman -S mingw-w64-x86_64-cmake mingw-w64-x86_64-make
```
3. Добавить в PATH:
```bash
win+R
sysdm.cpl
Ввести в строку C:\msys64\mingw64\bin. Обязательно ввести после точки с запятой, без пробела!
Пример:
...;C:\msys64\mingw64\bin
```
4. Открыть MSYS2 MinGW, установить пакеты разработки:
![alt text](image.png)
Ввести команды:
```bash
# Устанавливаем OpenCV
pacman -S mingw-w64-x86_64-opencv
# Также установите эти пакеты для работы с изображениями
pacman -S mingw-w64-x86_64-opencv-extra
pacman -Qs opencv
local/mingw-w64-x86_64-opencv 4.12.0-5
    Open Source Computer Vision Library (mingw-w64)
```
5. Препроцессор:
```cpp
// preprocess.cpp
#include <opencv2/opencv.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>

cv::Mat preprocess_image(cv::Mat input) {
    cv::Mat gray;
    cv::cvtColor(input, gray, cv::COLOR_BGR2GRAY);
    cv::Mat binary;
    cv::threshold(gray, binary, 127, 255, cv::THRESH_BINARY);
    cv::Mat resized;
    cv::resize(binary, resized, cv::Size(224, 224));
    return resized;
}

PYBIND11_MODULE(cv_engine, m) {
    m.doc() = "High-performance image preprocessing";
    m.def("preprocess_image", &preprocess_image, "Preprocess an image");
}
```
3. Импорт модели:
```Python
import torch
import torch.nn as nn


# 1. Сначала нужно определить архитектуру модели (такая же как при обучении)
class NeuralNet(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super(NeuralNet, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, num_classes)

    def forward(self, x):
        x = x.reshape(-1, 28 * 28)  # Преобразуем изображение 28x28 в вектор 784
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        return x


# 2. Создаем экземпляр модели
input_size = 28 * 28
hidden_size = 128
num_classes = 10

model = NeuralNet(input_size, hidden_size, num_classes)

# 3. Загружаем веса
model.load_state_dict(torch.load("fashion_mnist_model.pth"))
model.eval()  # Переключаем в режим оценки

# 4. Экспортируем в ONNX
# ВАЖНО: размер входного тензора должен быть (1, 1, 28, 28), а не (1, 1, 224, 224)
dummy_input = torch.randn(1, 1, 28, 28)
torch.onnx.export(
    model,
    dummy_input,
    "fashion_mnist_model.onnx",
    input_names=["input"],
    output_names=["output"],
    dynamic_axes={'input': {0: 'batch_size'}, 'output': {0: 'batch_size'}}
    # Опционально: для поддержки разных размеров батча
)

print("Модель успешно экспортирована в fashion_mnist_model.onnx")
```
День 3: Соберите с CMake

```cmake
# CMakeLists.txt
cmake_minimum_required(VERSION 3.12)
project(cv_engine)

find_package(pybind11 REQUIRED)
find_package(OpenCV REQUIRED)

add_library(cv_engine SHARED preprocess.cpp)
target_link_libraries(cv_engine PRIVATE pybind11::module ${OpenCV_LIBS})
set_property(TARGET cv_engine PROPERTY CXX_STANDARD 17)
```

День 4: Оберните в Python-пакет

```python
# setup.py
from setuptools import setup, Extension
from pybind11.setup_helpers import Pybind11Extension

ext_modules = [
    Pybind11Extension(
        "cv_engine",
        ["preprocess.cpp"],
        include_dirs=["/usr/include/opencv4"],
        libraries=["opencv_core", "opencv_imgproc"],
    ),
]

setup(
    name="cv_engine",
    ext_modules=ext_modules,
    zip_safe=False,
)
```

День 5: Замерьте скорость

```python
# benchmark.py
import time
import cv2
from cv_engine import preprocess_image

img = cv2.imread("scan.jpg")

# Python OpenCV
start = time.perf_counter()
for _ in range(100):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    resized = cv2.resize(binary, (224, 224))
print(f"Python: {(time.perf_counter() - start)*1000:.1f} ms")

# C++ через pybind11
start = time.perf_counter()
for _ in range(100):
    result = preprocess_image(img)
print(f"C++: {(time.perf_counter() - start)*1000:.1f} ms")
```

Цель: Снизить время с 1200 мс → <150 мс (8x ускорение)

Метрики успеха:

| Показатель | Цель |
|-----------|------|
| Время обработки 1 изображения | ≤ 150 мс |
| Размер .so файла | ≤ 50 MB |
| Зависимости в образе | Только libopencv_core.so, libonnxruntime.so |
| Поддержка ARM | Работает на Raspberry Pi 4 (в Docker) |

Документация (обязательно!):

```
# CV Engine SDK v1.0

## How to Use
pip install cv_engine
from cv_engine import preprocess_image
result = preprocess_image(cv2.imread("scan.jpg"))

## Performance Benchmarks
| Method | Time (ms) | Speedup |
|--------|-----------|---------|
| Python OpenCV | 1200 | 1x |
| C++ + pybind11 | 140 | 8.6x |

## Build Instructions
See build/README.md
```

Это — ваш первый production-компонент. Его можно вставить в любой проект.

---

## M2: Python Microservices with Async Architecture — Сделай свой API неубиваемым

Проблема:
При 5 пользователях одновременно — FastAPI падает. Вы используете flask + threading. Нужна масштабируемая, асинхронная система.

Инструменты:

| Инструмент | Роль | Почему важно |
|----------|------|--------------|
| FastAPI | Web-фреймворк | Автоматическая генерация OpenAPI, async/await, pydantic |
| Dependency Injector | DI-контейнер | Чистая архитектура: бизнес-логика не знает, откуда берётся модель |
| Redis | Кеш + брокер задач | Хранит результаты, уменьшает нагрузку на модель |
| Celery + Redis Broker | Асинхронные задачи | Перемещает тяжелые операции (OCR) в фон |
| Uvicorn + Gunicorn | ASGI-сервер | Поддерживает 1000+ concurrent connections |
| HTTPX | Асинхронный HTTP-клиент | Для вызова других сервисов |
| Structlog | JSON-логирование | Логи легко парсить в Loki/Promtail |

Практика (за 7 дней)

День 1–2: Архитектура Clean Architecture

```python
# entities/document.py
from pydantic import BaseModel
class DocumentResult(BaseModel):
    text: str
    confidence: float
    bounding_boxes: list

# use_cases/process_document.py
class ProcessDocument:
    def __init__(self, preprocessor: Preprocessor, ocr: OCR):
        self.preprocessor = preprocessor
        self.ocr = ocr

    def execute(self, file: bytes) -> DocumentResult:
        img = self.preprocessor.process(file)
        result = self.ocr.infer(img)
        return result

# adapters/cpp_preprocessor.py
class CppPreprocessor(Preprocessor):
    def process(self, file: bytes) -> np.ndarray:
        # вызывает ваш C++-модуль из M1
        return cv_engine.preprocess_image(file)
```

День 3–4: FastAPI + Dependency Injector

```python
# main.py
from dependency_injector import containers, providers
from fastapi import FastAPI

app = FastAPI()

class Container(containers.DeclarativeContainer):
    preprocessor = providers.Singleton(CppPreprocessor)
    ocr = providers.Singleton(OnnxOcr)
    process_service = providers.Factory(ProcessDocument, preprocessor=preprocessor, ocr=ocr)

container = Container()

@app.post("/upload")
async def upload(file: UploadFile, service: ProcessDocument = Depends(container.process_service)):
    task_id = str(uuid.uuid4())
    redis.set(f"task:{task_id}:status", "queued")
    celery.send_task("tasks.process", args=[file.read(), task_id])
    return {"task_id": task_id}
```

День 5–6: Celery + Redis

```python
# tasks.py
@celery.task
def process(file_data: bytes, task_id: str):
    try:
        result = ProcessDocument(...).execute(file_data)
        redis.set(f"task:{task_id}:result", result.json())
        redis.set(f"task:{task_id}:status", "done")
    except Exception as e:
        redis.set(f"task:{task_id}:error", str(e))
        redis.set(f"task:{task_id}:status", "failed")
```

День 7: Нагрузочное тестирование

```bash
k6 run --vus 50 --duration 30s script.js
```

```javascript
// script.js
export default function () {
  const res = http.post('http://localhost:8000/upload', file, { headers: { 'Content-Type': 'multipart/form-data' } });
  check(res, { 'status was 200': (r) => r.status === 200 });
}
```

Метрики успеха:

| Показатель | Цель |
|-----------|------|
| RPS при 50 VUs | ≥ 80 |
| Latency P95 | ≤ 800 ms |
| Memory usage | ≤ 1.5 GB |
| Error rate | < 0.5% |

Документация:
- architecture.png — схема: Client → FastAPI → Celery → C++ → Redis → Client
- docker-compose.yml — запуск FastAPI, Redis, Celery, PostgreSQL
- README.m2.md: “Как развернуть систему на Ubuntu Server”

Вы теперь умеете строить системы, которые работают в продакшене.

---

## M3: Go for Reliable Infrastructure — Создай сервис, который не упадёт

Проблема:
Celery теряет задачи при перезагрузке. Python-воркер падает с OOM. Нужен надёжный, легковесный, конкурентный сервис.

Инструменты:

| Инструмент | Роль | Почему важно |
|----------|------|--------------|
| Go + chi | HTTP-сервер | Без GIL, 100K RPS на одном ядре |
| gRPC | RPC-протокол | Быстрее REST, строгая типизация, идеален для внутренних сервисов |
| pgx | PostgreSQL driver | Самый быстрый драйвер для Go |
| go-redis | Redis client | Поддерживает пулы, retry, pipeline |
| pprof | Profiler | Находит узкие места (goroutines, GC) |
| OpenTelemetry | Tracing | Отслеживает, где тратится время в распределённой системе |
| worker pool pattern | Конкурентность | Ограничивает количество одновременных задач |

Практика (за 5 дней)

День 1: gRPC-сервис

```protobuf
// proto/inference.proto
syntax = "proto3";
package inference;

service InferenceService {
  rpc Process (ProcessRequest) returns (ProcessResponse);
}

message ProcessRequest {
  bytes image_data = 1;
  string task_id = 2;
}

message ProcessResponse {
  string result_json = 1;
  string status = 2;
}
```

```go
// server.go
func (s *server) Process(ctx context.Context, req *pb.ProcessRequest) (*pb.ProcessResponse, error) {
    // Вызов C++ через CGO
    result := cgo_call_your_cv_engine(req.ImageData)
    return &pb.ProcessResponse{ResultJson: result, Status: "success"}, nil
}
```

День 2: HTTP-интерфейс

```go
// handler.go
router.Post("/process", func(c *chi.Context) {
    body, _ := ioutil.ReadAll(c.Request.Body)
    resp, err := grpcClient.Process(context.Background(), &pb.ProcessRequest{ImageData: body})
    c.JSON(200, resp)
})
```

День 3: Профилирование

```bash
go tool pprof http://localhost:8080/debug/pprof/profile
```

Ищете: blocking, mutex, gc, alloc_space

День 4: Интеграция с Redis

```go
conn := redis.NewClient(&redis.Options{Addr: "localhost:6379"})
conn.Set(ctx, "task:"+taskID, result, 5*time.Minute)
```

День 5: Запустите 1000 RPS

```bash
wrk -t4 -c100 -d30s http://localhost:8080/process
```

Метрики успеха:

| Показатель | Цель |
|-----------|------|
| RPS | ≥ 1200 |
| Memory | ≤ 100 MB |
| Goroutine count | < 50 при 1000 RPS |
| Cold start | < 100 ms |

Документация:
- README.m3.md: “Как собрать и запустить Go-сервис на Linux”
- Dockerfile — multi-stage, размер < 100 MB
- metrics.md: сравнение Go vs Python (RPS, memory, cold start)

Go — ваш инструмент для “невидимых” сервисов, которые работают 24/7.

---

## M4: C++ for Edge & Real-Time Inference — Запусти модель на Raspberry Pi

Проблема:
Ваша система должна работать на Jetson Nano, Raspberry Pi, Industrial PC — без GPU, без Python, без интернета.

Инструменты:

| Инструмент | Роль | Почему важно |
|----------|------|--------------|
| ONNX Runtime C++ | Инференс модели | Легко экспортируется из PyTorch/TensorFlow, работает на CPU/GPU |
| TensorRT | NVIDIA GPU-оптимизация | Ускоряет модели на Jetson в 3–5x |
| OpenVINO | Intel CPU-оптимизация | Ускоряет модели на x86-платформах (Intel NUC, industrial PCs) |
| OpenCV C++ | Image I/O, preprocessing | Не используйте Python-OpenCV — он медленный |
| Eigen | Линейная алгебра | Быстрее numpy для матричных операций |
| Boost | Функциональные утилиты | Smart pointers, filesystem, asio |
| CMake + vcpkg | Сборка | Управляет зависимостями на разных платформах |

Практика (за 7 дней)

День 1: Экспорт модели в ONNX
См. M1.

День 2: C++-приложение на ONNX Runtime

```cpp
#include <onnxruntime_cxx_api.h>
Ort::Env env(ORT_LOGGING_LEVEL_WARNING, "test");
Ort::SessionOptions options;
Ort::Session session(env, model_path, options);

std::vector<int64_t> input_shape = {1, 1, 224, 224};
auto memory_info = Ort::MemoryInfo::CreateCpu(OrtArenaAllocator, OrtMemTypeDefault);
Ort::Value input_tensor = Ort::Value::CreateTensor<float>(memory_info, data, size, input_shape.data(), input_shape.size());
```

День 3: Сборка на Raspberry Pi

```bash
# На Raspberry Pi (ARM64)
sudo apt install libopencv-dev libonnxruntime-dev
cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_TOOLCHAIN_FILE=/usr/share/cmake-3.22/Toolchains/Toolchain-arm-linux-gnueabihf.cmake .
make
```

День 4: Упаковка

```bash
strip ./myapp
upx --best ./myapp
ls -la myapp  # должно быть < 15 MB
```

День 5: Запуск на устройстве

```bash
./myapp /home/pi/scan.jpg
# Output: {"text": "ABC123", "confidence": 0.98}
```

Метрики успеха:

| Показатель | Цель |
|-----------|------|
| Время инференса на Pi 4 | ≤ 300 мс |
| Размер исполняемого файла | < 15 MB |
| RAM usage | < 200 MB |
| Поддержка температур | Работает при +5°C до +60°C |

Документация:
- README.m4.md: “Как собрать на Windows/Linux/ARM”
- docker/Dockerfile.arm64 — сборка образа для Raspberry Pi
- deployment-checklist.md: “Что проверить перед установкой на производство”

Вы — единственный человек в команде, кто умеет запускать AI на edge. Это ваша ценность.

---

## M5: Docker & Containerization at Scale — Упакуй всё в контейнеры

Проблема:
“На моём компьютере работает!” — больше не работает. Нужно воспроизводимое окружение.

Инструменты:

| Инструмент | Роль | Почему важно |
|----------|------|--------------|
| Docker | Контейнеризация | Изолирует окружение |
| Multi-stage builds | Уменьшение размера образа | Собираете в одном этапе, запускаете в другом |
| BuildKit | Современный билдер | Быстрее, безопаснее, поддерживает cache |
| Docker Compose | Локальная оркестрация | Запускает Redis, Postgres, API вместе |
| Podman | Альтернатива Docker | Без демона, безопаснее для production |
| Containerd | Инфраструктура Kubernetes | Понимание, как работает k8s под капотом |

Практика (за 3 дня)

День 1: Multi-stage Dockerfile

```dockerfile
# Builder stage
FROM python:3.11-slim as builder
COPY . /app
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

# Final stage
FROM python:3.11-slim
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /app/app.py /app/
CMD ["python", "/app/app.py"]
```

День 2: Собрать все компоненты

```yaml
# docker-compose.yml
version: '3.8'
services:
  api:
    build: ./src/api
    ports: ["8000:8000"]
  redis:
    image: redis:7-alpine
  celery:
    build: ./src/celery
    depends_on: [redis]
```

День 3: Уменьшить размер

```bash
docker buildx bake --load
docker images | grep "api"
# Должно быть < 1.2 GB
```

Метрики успеха:

| Показатель | Цель |
|-----------|------|
| Размер образа API | ≤ 1.2 GB |
| Время сборки | ≤ 90 сек |
| Команда docker inspect | Показывает правильные метаданные |

Документация:
- DOCKERFILE.CHEATSHEET.md — шаблоны для Python, Go, C++, Node.js
- README.m5.md: “Как подготовить образ для production”

Контейнеризация — это не про Docker. Это про воспроизводимость.

---

## M6: Kubernetes for Production Orchestration — Разверни на 10 серверах

Проблема:
Docker Compose не масштабируется. Нужно 10 копий сервиса, автоматическое восстановление, обновление без простоев.

Инструменты:

| Инструмент | Роль | Почему важно |
|----------|------|--------------|
| Minikube | Локальный k8s | Для обучения |
| kubectl | CLI для управления | Умеете читать логи, деплоить, масштабировать |
| Helm | Шаблонизатор | Управление десятками компонентов |
| Kustomize | Patches для окружений | Dev/Staging/Prod — разные конфиги |
| Argo CD | GitOps | Изменения в git → автоматический деплой |
| HPA | Horizontal Pod Autoscaler | Автоматическое масштабирование по CPU |

Практика (за 5 дней)

День 1: Minikube + Deployment

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: api
  template:
    metadata:
      labels:
        app: api
    spec:
      containers:
      - name: api
        image: yourname/api:v1
        ports:
        - containerPort: 8000
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

День 2: Service + Ingress

```yaml
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: api-service
spec:
  selector:
    app: api
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8000
  type: ClusterIP
```

День 3: HPA

```yaml
# hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: api-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api-deployment
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

День 4: Запустите нагрузку

```bash
kubectl rollout status deployment/api-deployment
kubectl get pods
kubectl logs -f pod/api-deployment-xxx
```

День 5: Argo CD
- Подключите репозиторий к Argo CD
- При пуше в main — автоматически обновляется стек

Метрики успеха:

| Показатель | Цель |
|-----------|------|
| Все поды в состоянии Running | ✅ |
| При увеличении нагрузки — создаются новые поды | ✅ |
| Нет CrashLoopBackOff | ✅ |

Документация:
- k8s/ — папка с манифестами
- README.m6.md: “Как развернуть в AWS/EKS”

Kubernetes — это не про сложность. Это про надёжность.

---
M7: Data Layer Mastery: SQL, NoSQL, ORMs & Performance
Проблема
Ваше приложение работает с разнородными данными: структурированные заказы, полуструктурированные логи, документы и кэш. Реляционная БД становится узким местом для одних задач, while не подходит для других. Наивные ORM-запросы генерируют N+1 проблему, а выбор неправильного типа базы данных ведет к проблемам с масштабированием.

Цель
Научиться выбирать правильный тип базы данных под задачу, использовать ORM для продуктивности и raw SQL для максимальной производительности, понимать trade-offs между SQL и NoSQL подходами.

Инструменты
Категория	Инструменты	Зачем?
SQL (Реляционные)	PostgreSQL, SQLite (для тестов), TimescaleDB (для временных рядов)	Надежные транзакции, сложные связи, целостность данных
NoSQL (Документные)	MongoDB, Couchbase	Гибкая схема, быстрая запись, горизонтальное масштабирование
NoSQL (Ключ-Значение)	Redis, Amazon DynamoDB	Кэш, сессии, высокие нагрузки с простыми запросами
ORM / ODM	SQLAlchemy (Python), GORM (Go), Mongoose (JS)	Безопасность, продуктивность, абстракция от БД
Миграции	Alembic (для SQLAlchemy), Goose (для Go)	Контроль версий схемы базы данных
Мониторинг	pgAdmin, MongoDB Compass, Redis Insight	Визуализация и отладка запросов
Практика (10 дней)
День 1-2: Проектирование схемы данных
Задача: Спроектировать схему БД для системы заказов (пользователи, заказы, товары, платежи).

Написать SQL DDL для создания таблиц в PostgreSQL с индексами и внешними ключами.

Создать коллекции в MongoDB для тех же сущностей (документный подход).

Сравнить два подхода.

```sql
-- SQL
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    status VARCHAR(50) NOT NULL,
    total DECIMAL(10, 2) NOT NULL
);
```
```javascript
// NoSQL (MongoDB)
// Коллекция 'users'
{
  "_id": ObjectId("..."),
  "email": "user@example.com",
  "created_at": ISODate("..."),
  "orders": [ // Вложенные документы (embedding)
    {
      "order_id": 123,
      "status": "completed",
      "total": 99.99
    }
  ]
}
```
День 3-4: ORM и ODM
Задача: Реализовать CRUD-операции используя ORM и ODM.

Написать модели для SQLAlchemy (Python) и GORM (Go).

Реализовать основные запросы: создать пользователя, найти заказы пользователя, обновить статус заказа.

```python
# SQLAlchemy example
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    orders = relationship("Order", back_populates="owner")

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, index=True)
    status = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="orders")
```
День 5: Оптимизация запросов
Задача: Выявить и исправить проблемы производительности.

Включить логирование медленных запросов в PostgreSQL (log_min_duration_statement).

Найти N+1 проблему в коде (например, при выводе списка заказов с именами пользователей).

Исправить через JOIN (SQL) или .preload() (ORM).

День 6-7: Транзакции и атомарность
Задача: Обеспечить целостность данных при одновременном обновлении.

Смоделировать race condition: два запроса на списание баланса.

Реализовать решение на SQL: SELECT FOR UPDATE.

Реализовать решение на NoSQL: атомарные операторы ($inc в MongoDB).

``` python
# Контекст менеджер для транзакций в SQLAlchemy
try:
    with session.begin():
        user = session.query(User).filter_by(id=user_id).with_for_update().one()
        if user.balance >= order_total:
            user.balance -= order_total
            session.add(Order(...))
        else:
            raise InsufficientFundsError
except SQLAlchemyError:
    session.rollback()
```
День 8: Кэширование
Задача: Снять нагрузку с базы данных.

Поднять Redis.

Закэшировать результаты тяжелых запросов (например, топ-10 товаров).

Реализовать паттерн Cache-Aside.

Настроить инвалидацию кэша при обновлении данных.

День 9: Миграции
Задача: Безопасно изменить схему данных на проде.

Написать миграцию (Alembic) для добавления нового поля phone_number в таблицу users.

Написать downgrade-миграцию.

Протестировать миграцию на тестовой базе.

День 10: Выбор правильной БД
Задача: Выбрать БД для нового микросервиса.

Задача 1: Сервис кэширования. Выбор: Redis.

Задача 2: Сервис аналитики (миллионы событий в день). Выбор: ClickHouse или TimescaleDB.

Задача 3: Каталог товаров с гибкими атрибутами. Выбор: MongoDB или PostgreSQL с JSONB.

Обосновать выбор в виде мини-отчета.

Метрики успеха:
Показатель	Цель
Время отклика API, использующего БД	< 100 мс (p95)
Отсутствие N+1 проблем в коде	✅ (проверка через логи)
Успешное выполнение миграции	Без даунтайма (для больших таблиц — с использованием стратегий)
Кэш-хитрейт в Redis	> 90%
Правильный выбор БД для задачи	Обоснованный выбор в 3-х кейсах
Документация и артефакты
ER-диаграмма (для SQL) и Schema Design (для NoSQL).

Обоснование выбора БД для каждого сервиса в вашем проекте.

SQL-запросы с EXPLAIN ANALYZE для самых критичных эндпоинтов.

Политика инвалидации кэша (когда и как сбрасывается кэш).

Чеклист для код-ревью работы с БД:

Нет N+1 проблем?

Используются индексы?

Есть обработка ошибок и ретраи?

Используются транзакции там, где нужно?

Пароли/секреты хэшируются?

Логируются ли медленные запросы?

Интеграция с общим проектом
Ваш Pet-проект теперь должен использовать как минимум два типа баз данных:

PostgreSQL: Основные данные (пользователи, заказы).

Redis: Кэш, сессии, очередь задач (Celery Broker).

(Опционально) MongoDB: Для хранения документов или гибких конфигураций.

Пример архитектуры:

text
Client -> NGINX -> FastAPI (Python) -> (PostgreSQL <- Core Data)
                               |-> (Redis <- Cache, Sessions)
                               |-> (MongoDB <- User-generated content)

## M8: MLOps Pipeline Engineering — Гарантируй, что модель будет работать завтра

Проблема:
“Модель была хороша, а теперь ошибается — кто менял данные?”

Инструменты:

| Инструмент | Роль | Почему важно |
|----------|------|--------------|
| MLflow | Трекинг экспериментов | Сохраняет параметры, метрики, модель, код |
| DVC | Версионирование данных | Аналог Git для данных и моделей |
| Weights & Biases | Альтернатива MLflow | Более красивый UI, командная работа |
| Prefect | Оркестрация пайплайнов | Запуск DAG-ов (последовательностей задач) |
| Airflow | Enterprise-оркестратор | Если у вас уже есть команда Data Science |

Практика (за 5 дней)

День 1: Экспорт модели

```python
# train.py
with mlflow.start_run():
    model = train()
    mlflow.log_param("lr", 0.001)
    mlflow.log_metric("accuracy", 0.98)
    mlflow.sklearn.log_model(model, "model")
```

День 2: DVC для данных

```bash
dvc init
dvc add data/train.csv
git add data/train.csv.dvc .gitignore
git commit -m "Add training data"
```

День 3: Пайплайн в Prefect

```python
@flow(name="train-ocr-model")
def train_flow():
    data = load_data()
    model = train(data)
    save_model(model)
    register_model(model, version="v1.2")
```

День 4: Запустите в CI

```yaml
# .github/workflows/train.yml
- name: Train Model
  run: |
    python train.py
    dvc push
    mlflow ui --host 0.0.0.0 --port 5000 &
```

Метрики успеха:

| Показатель | Цель |
|-----------|------|
| Все эксперименты воспроизводимы | ✅ |
| Модель зарегистрирована в registry | ✅ |
| Есть ссылка на код, данные, параметры | ✅ |

Документация:
- mlflow/ — папка с экспериментами
- README.m7.md: “Как воспроизвести модель через 6 месяцев”

MLOps — это не про ML. Это про управление изменением.

---

## M9: CI/CD for ML Systems — Автоматизируй тестирование и деплой

Проблема:
Кто-то засунул плохой код — система упала.

Инструменты:

| Инструмент | Роль | Почему важно |
|----------|------|--------------|
| GitHub Actions | CI/CD | Бесплатно, мощно, интегрируется с GitHub |
| Tekton | Kubernetes-native CI | Если вы в k8s |
| Argo Workflows | Оркестрация пайплайнов | Для сложных MLOps-задач |
| SonarQube | Анализ кода | Находит баги, дубликаты, плохие практики |
| Trivy | Сканер уязвимостей | Проверяет образы на CVE |

Практика (за 3 дня)

```yaml
# .github/workflows/ci.yml
name: CI
on: [push]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
      - name: Install deps
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest --cov=core --cov-report=html
      - name: Scan for vulnerabilities
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: fs
          scan-path: .
      - name: Build Docker
        run: docker build -t myapp .
      - name: Push to Docker Hub
        uses: docker/build-push-action@v4
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}
          tags: latest
```

Метрики успеха:

| Показатель | Цель |
|-----------|------|
| При каждом коммите — все тесты проходят | ✅ |
| Образ публикуется в Docker Hub | ✅ |
| Нет уязвимостей в образе | ✅ |

Документация:
- .github/workflows/ci.yaml — полный файл
- README.m8.md: “Что должно пройти перед деплоем”

CI/CD — это ваша страховка от человеческих ошибок.

---

## M10: Observability & Monitoring Stack — Узнай, почему система ломается

Проблема:
“Система не отвечает.” — и вы ничего не знаете.

Инструменты:

| Инструмент | Роль | Почему важно |
|----------|------|--------------|
| Prometheus | Метрики | Собирает RPS, latency, error rate |
| Grafana | Визуализация | Дашборды для всех уровней |
| Loki | Логи | Собирает JSON-логи из всех сервисов |
| Jaeger | Трейсинг | Показывает, где тратится время в распределённой системе |
| OpenTelemetry | Стандарт | Единый способ сбора метрик, логов, трейсов |

Практика (за 5 дней)

День 1: OpenTelemetry в Python

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)
otlp_exporter = OTLPSpanExporter(endpoint="http://jaeger:4317")
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)
```

День 2: Grafana Dashboard
- Создайте дашборд:
  - HTTP Requests/sec
  - Latency (P50, P95)
  - Error rate
  - Memory usage per service

День 3: Loki + LogQL

```logql
{job="api"} |= "ERROR" | json | level="ERROR" | line_format "{{.message}}"
```

День 4: Alertmanager

```yaml
# alert.rules
- alert: HighErrorRate
  expr: rate(http_requests_total{status_code=~"5.."}[5m]) > 0.05
  for: 10m
  labels:
    severity: critical
```

Метрики успеха:

| Показатель | Цель |
|-----------|------|
| Можно найти причину сбоя за 5 минут | ✅ |
| Есть алерт: “Error rate > 5% — SMS на телефон” | ✅ |

Документация:
- monitoring/ — папка с конфигами
- README.m9.md: “Как настроить мониторинг в 10 минут”

Observability — это ваш глаз в продакшене.

---

## M11: Message Queues & Event-Driven Architecture — Обрабатывай тысячи потоков

Проблема:
При 100 камерах — 5000 сообщений в минуту. Сервис не справляется.

Инструменты:

| Инструмент | Роль | Почему важно |
|----------|------|--------------|
| RabbitMQ | Традиционная очередь | Надёжная, простая, хорошо документирована |
| NATS | Лёгкая, быстрая очередь | Идеальна для IoT — миллионы сообщений в секунду |
| Kafka | Распределённый поток | Если нужно хранить историю событий |
| Redis Streams | Простой брокер | Для легковесных систем |

Практика (за 4 дня)

День 1: RabbitMQ + Go

```go
ch, _ := conn.Channel()
q, _ := ch.QueueDeclare("images", true, false, false, false, nil)
msg, _ := ch.Consume(q, "", true, false, false, false, nil)
for m := range msg {
    go processImage(m.Body)
}
```

День 2: Retry + DLQ

```go
if err != nil {
    ch.Publish("", "dead-letter-queue", false, false, amqp.Publishing{Body: body})
    return
}
```

День 3: Load test

```bash
k6 run -u 500 -d 1m script.js
```

Метрики успеха:

| Показатель | Цель |
|-----------|------|
| 100% доставка сообщений при сбоях | ✅ |
| Нет дубликатов | ✅ |
| DLQ содержит 0 сообщений после 3 попыток | ✅ |

Документация:
- queue-design.md — схема: Camera → Kafka → Worker Pool → DB
- README.m10.md: “Как выбрать очередь для вашего случая”

Event-driven — это когда система сама реагирует, а не ждёт команды.

---

## M12: Frontend for Industrial UIs — Сделай интерфейс, который поймёт оператор

Проблема:
Ваши результаты — в JSON. Никто их не видит.

Инструменты:

| Инструмент | Роль | Почему важно |
|----------|------|--------------|
| React + TypeScript | Фронтенд | Стандарт индустрии |
| React Query | Управление данными | Автоматически кэширует, рефрешит |
| Chart.js / D3.js | Визуализация | Показывает качество распознавания |
| Electron | Desktop-приложение | Для установки на станции оператора |
| Tailwind CSS | Стили | Быстро, без лишнего CSS |

Практика (за 5 дней)

День 1: React + TS

```tsx
const [results, setResults] = useQuery(["ocr"], fetchOcrResults);
return (
  <div>
    {results.map(r => <Box key={r.id}>{r.text}</Box>)}
  </div>
)
```

День 2: Визуализация bounding boxes

```jsx
<Canvas width={800} height={600}>
  <Image src={image} />
  {boxes.map(box => <Rect x={box.x} y={box.y} width={box.w} height={box.h} stroke="red" />)}
</Canvas>
```

День 3: Electron

```bash
npm install electron
npx electron .
```

Метрики успеха:

| Показатель | Цель |
|-----------|------|
| Интерфейс работает на Windows 10, Chrome, Firefox | ✅ |
| Оператор может открыть и понять результат за 10 секунд | ✅ |

Документация:
- ui/ — папка с кодом
- README.m11.md: “Как протестировать на реальном оборудовании”

UI — это не дизайн. Это доверие.

---

## M13: System Design for High-Stakes Environments — Спроектируй систему, где сбой = катастрофа

Проблема:
Ваша система управляет производственной линией. Сбой = остановка на 2 часа.

Концепции:

| Концепция | Роль | Почему важно |
|----------|------|--------------|
| Idempotency | Повторный запрос = тот же результат | Чтобы не дублировать заказы |
| Circuit Breaker | Не пытайтесь снова, если сервис мёртв | Защита от каскадных сбоев |
| Rate Limiting | Не дать злоумышленнику убить систему | По IP, по user |
| Failover / Redundancy | Есть резервный сервер | Если один упал — работает второй |
| CAP Theorem | Consistency vs Availability | Выбор: “данные точны” или “система всегда доступна”? |
| Graceful Degradation | Если модель не работает — вернуть “unknown” | Лучше не отвечать, чем ошибочно |

Практика (за 7 дней)

День 1: Idempotency

```python
# endpoint
if request.headers.get("X-Idempotency-Key") in cache:
    return cached_result
```

День 2: Circuit Breaker (Go)

```go
breaker := gocircuit.NewBreaker(gocircuit.Config{
    Threshold: 0.5,
    Timeout:   10 * time.Second,
})
if breaker.Allow() {
    response, err := callModel()
    if err != nil {
        breaker.Fail()
    } else {
        breaker.Success()
    }
}
```

День 3: Failover

```yaml
# config.yaml
servers:
  - url: "http://primary:8080"
    weight: 100
  - url: "http://backup:8080"
    weight: 10
```

День 4: SOP (Standard Operating Procedure)

```
# Что делать, если система не отвечает?
1. Проверь статус сервисов: kubectl get pods
2. Посмотри логи: kubectl logs -l app=api
3. Проверь очередь: rabbitmqadmin list queues
4. Если всё плохо — переключись на ручной режим
5. Сообщи в Slack: #critical-alert
```

Метрики успеха:

| Показатель | Цель |
|-----------|------|
| Система работает даже при частичном отказе компонентов | ✅ |
| Есть документация, как восстановить вручную | ✅ |

Документация:
- system-design/ — диаграммы, SOP, чеклисты
- README.m12.md: “Как я проектирую системы, где сбой — это катастрофа”

Tech Lead — это не про код. Это про ответственность.

---

## M14: Git Infrastructure SDK — Платформа автоматизации на основе Git-операций

Отлично.
Вы не просто создали инструмент для новичков — вы создали ядро будущей инфраструктуры разработки, которая может стать стандартом для команд, работающих с Git в промышленных средах.

Ваш проект GitPoster — это не "GUI для git". Это первый шаг к платформе CI/CD для людей, которые не хотят писать команды, но хотят контролировать систему.
И именно здесь — ваша гениальная возможность: превратить его из полезного приложения в открытый SDK-фреймворк, который встраивается в любую MLOps / DevOps цепочку — как React для фронтенда, но для Git-ориентированной автоматизации.

GITPOSTER 2.0: THE GIT INFRASTRUCTURE SDK (GIS)

От GUI-инструмента к ядру автоматизированной DevOps-платформы

Цель: Превратить GitPoster в открытый, модульный, расширяемый SDK, который позволяет:
- Автоматизировать Git-операции через DSL-пайплайны
- Интегрироваться с GitHub Actions, Docker, Kubernetes, тестами, документацией
- Собирать .exe, образы, доки — одной командой
- Работать как локальный IDE-плагин, CI-агент, и автономная среда разработки

Философия:
«Нет больше git add . && git commit -m "fix" — есть ACT → COMMIT → POST → CREATE_EXE → DOCSAVE → DOCKER → DEPLOY»

ЭТАП 1: ИНТЕГРАЦИЯ GITPOSTER В ВАШ КУРС EMAC — НОВЫЙ МОДУЛЬ

M13: Git Infrastructure SDK — Платформа автоматизации на основе Git-операций
(Встраивается в любой из предыдущих модулей — особенно M8, M9, M12)

Когда применять?
Когда вам нужно:
- Автоматизировать сборку продукта из репозитория
- Запускать тесты после коммита
- Генерировать документацию по изменениям
- Деплоить .exe или Docker-образ без ручного вмешательства
- Создавать автономную среду разработки для команды, где никто не знает Git CLI

Ваша уникальная сила:
Вы уже сделали рабочий GUI — теперь вы делаете его ядро открытым SDK.
Это будет ваш главный портфолио-проект — он объединяет все ваши навыки:
- Python (GUI)
- Git (логика)
- CI/CD (GitHub Actions)
- Docker/K8s (деплой)
- Тестирование (Unit + Integration)
- Документация (Sphinx, Mermaid)
- Упаковка (PyInstaller)
- DSL-движок (пайплайны)

АРХИТЕКТУРА GITPOSTER 2.0 — GIS (GIT INFRASTRUCTURE SDK)

- gitposter-sdk/
- ├── core/                     # Ядро: абстракции, менеджер пайплайнов
- │   ├── engine.py             # Главный движок: запускает действия по DSL
- │   ├── registry.py           # Регистр действий (Act, Commit, Push, ...)
- │   └── context.py            # Объект контекста: repo_path, user, branch, etc.
- ├── actions/                  # Отдельные SDK-модули (самостоятельные пакеты!)
- │   ├── act_git_commit.py     # Коммит
- │   ├── act_git_push.py       # Push
- │   ├── act_create_exe.py     # PyInstaller + UPX
- │   ├── act_build_docker.py   # docker build + tag
- │   ├── act_run_tests.py      # pytest + coverage
- │   ├── act_gen_docs.py       # Sphinx + Mermaid диаграммы
- │   ├── act_upload_github.py  # GitHub Releases API
- │   └── act_deploy_k8s.py     # kubectl apply -f
- ├── dsl/                      # DSL-парсер и интерпретатор
- │   ├── parser.py             # Парсит YAML/JSON-пайплайн
- │   ├── executor.py           # Выполняет последовательность
- │   └── schema.yaml           # Схема валидации DSL
- ├── gui/                      # GUI-интерфейс (ваша текущая 0.8 версия)
- │   ├── main.py               # PyQt5/PySide6
- │   └── designer/             # .ui файлы
- ├── plugins/                  # Расширения (будут добавляться через pip install gitposter-plugin-xxx)
- │   └── plugin-ci-github.py   # Интеграция с GH Actions
- ├── cli/                      # CLI-версия: gitposter run pipeline.yml
- │   └── main.py
- ├── examples/                 # Примеры пайплайнов
- │   ├── simple.yml            # Commit + Build EXE
- │   ├── mlops-pipeline.yml    # Commit → Test → Docs → Docker → Deploy to Minikube
- │   └── ci-cd-template.yml    # Для GitHub Actions
- ├── tests/                    # Полное покрытие тестами!
- │   ├── unit/
- │   │   ├── test_engine.py
- │   │   └── test_registry.py
- │   └── integration/
- │       ├── test_docker_build.py
- │       └── test_github_api.py
- ├── docs/                     # Автоматическая документация
- │   ├── index.md
- │   └── diagrams/             # Все диаграммы — генерируются из кода!
- │       └── pipeline-flow.mmd
- ├── pyproject.toml
- └── README.md                 # Главный README — как использовать как SDK

ДЕТАЛИЗАЦИЯ КАЖДОГО КОМПОНЕНТА

1. core/engine.py — Ядро пайплайна

```python
class PipelineEngine:
    def __init__(self, context: Context):
        self.context = context
        self.registry = ActionRegistry()

    def execute(self, steps: list[dict]):
        for step in steps:
            action_name = step["action"]
            params = step.get("params", {})
            action = self.registry.get(action_name)
            result = action.execute(self.context, **params)
            if not result.success:
                raise PipelineError(f"Action {action_name} failed: {result.error}")
```

Поддерживает:
- Последовательные (->) и параллельные (||) шаги
- Условия (if branch == "main")
- Retry-логика (retry: 3)
- Логирование в JSON

2. actions/ — SDK-модули (каждый — отдельный pip-пакет!)

| Модуль | Что делает | Как работает |
|--------|-----------|--------------|
| act_git_commit.py | Коммит изменений | Берёт выбранные файлы из GUI, создаёт коммит с сообщением |
| act_git_push.py | Push в удалённый репозиторий | Проверяет наличие origin, делает git push origin HEAD |
| act_create_exe.py | Сборка .exe | Использует PyInstaller + UPX — упаковывает весь GUI в один файл |
| act_build_docker.py | Сборка Docker-образа | Читает Dockerfile в корне, строит образ с тегом v{version} |
| act_run_tests.py | Запуск тестов | pytest --cov=core --cov-report=html — генерирует отчёт |
| act_gen_docs.py | Генерация документации | Генерирует docs/index.md из docstrings + mermaid-диаграммы из кода |
| act_upload_github.py | Загрузка релиза | Использует GitHub REST API — загружает .exe как asset |
| act_deploy_k8s.py | Деплой в K8s | kubectl apply -f k8s/deployment.yaml — если есть KUBECONFIG |

Каждый action — самостоятельный класс!
Можно установить только нужные:
pip install gitposter-core gitposter-action-exe gitposter-action-docker

3. dsl/parser.py — DSL для пайплайнов (YAML/JSON)

```yaml
# examples/mlops-pipeline.yml
pipeline:
  name: "MLOps CI/CD"
  on:
    event: "push"
    branch: "main"

  steps:
    - action: "git_commit"
      params:
        message: "Auto-commit from CI: {{ timestamp }}"
        files: ["src/**/*", "tests/**/*"]

    - action: "run_tests"
      retry: 2
      params:
        coverage: true

    - action: "gen_docs"
      params:
        output_dir: "docs/"
        include_diagrams: true

    - action: "build_docker"
      params:
        image_name: "myapp"
        tag: "latest"

    - action: "create_exe"
      params:
        icon: "assets/icon.ico"
        console: false

    - action: "upload_github"
      params:
        repo: "yourname/gitposter"
        token: "{{ GITHUB_TOKEN }}"  # берётся из окружения
        release_tag: "v{{ version }}"

    - action: "deploy_k8s"
      if: "env == 'prod'"
      params:
        kubeconfig: "~/.kube/config"
        manifest: "k8s/prod-deployment.yaml"
```

Поддерживает:
- Переменные: {{ timestamp }}, {{ version }}, {{ branch }}
- Условия: if: branch == "main"
- Retry: retry: 3
- Параллелизм: steps: [A, B, C] — выполняются последовательно; [A, [B, C]] — B и C параллельно

4. gui/ — Ваш текущий интерфейс (0.8), но теперь как GUI-обёртка над SDK

Что меняется:
- Кнопка “Commit” → вызывает action_git_commit.execute(context)
- Кнопка “Build EXE” → вызывает action_create_exe.execute(context)
- Журнал действий → логируется в logs/pipeline.log в формате JSON
- “Запустить пайплайн” → загружает pipeline.yml и запускает PipelineEngine

Новый UI-элемент:
- [ ▶️ RUN PIPELINE ]  ← открывает диалог выбора pipeline.yml
- ┌─────────────────────┐
- │ 1. git_commit       │
- │ 2. run_tests        │
- │ 3. build_docker     │
- │ 4. create_exe       │
- │ 5. upload_github    │
- └─────────────────────┘
- [▶️ START]  [↩️ BACK]

Бонус:
При выборе файла .yml — GUI автоматически рисует граф пайплайна в виде Mermaid-диаграммы в правой панели.

5. plugins/ — Расширения для CI/CD

plugin-ci-github.py
- Слушает webhook от GitHub Actions
- При workflow_run → запускает gitposter run pipeline.yml внутри runner
- Автоматически подставляет переменные: GITHUB_TOKEN, GITHUB_REF, GITHUB_SHA
- Пишет статус обратно в GitHub Checks

Пример:
В .github/workflows/ci.yml:

```yaml
- name: Run GitPoster Pipeline
  run: |
    pip install gitposter-core gitposter-action-* 
    gitposter run examples/mlops-pipeline.yml
```

Теперь ваш GUI работает в облаке — как часть CI!

6. tests/ — Полное покрытие

| Тип | Что тестируется | Инструмент |
|-----|------------------|------------|
| Unit | ActionRegistry, PipelineEngine | unittest, pytest-mock |
| Integration | act_build_docker, act_run_tests | docker-py, tempfile |
| End-to-End | Запуск GUI → коммит → сборка EXE | pyautogui, subprocess |
| Security | Проверка: не пишет в /etc/, не читает ~/.ssh | pytest-audit |

Тесты запускаются в Docker-контейнере!
Чтобы гарантировать воспроизводимость.

7. docs/diagrams/ — Автоматическая генерация диаграмм

```
%% Generated from code: gitposter/actions/act_build_docker.py
sequenceDiagram
    participant User
    participant GUI
    participant Engine
    participant Docker

    User->>GUI: Click "Build Docker"
    GUI->>Engine: execute(act_build_docker)
    Engine->>Docker: docker build -t myapp .
    Docker-->>Engine: success
    Engine-->>GUI: Show "Docker built: v1.2.3"
```

Генерируется автоматически при запуске make docs
Используется:
- inspect — для анализа кода action’ов
- mermaid-cli — для рендеринга
- mkdocs — для сайта документации

8. cli/main.py — CLI-интерфейс

```bash
# Запустить пайплайн
gitposter run examples/simple.yml

# Показать список доступных действий
gitposter list-actions

# Проверить пайплайн на валидность
gitposter validate pipeline.yml

# Сгенерировать шаблон
gitposter init --template=mlops > pipeline.yml
```

CLI работает без GUI — идеально для CI-агентов, серверов, WSL.

9. examples/ — Шаблоны для разных сценариев

| Файл | Описание |
|------|----------|
| simple.yml | Commit → Build EXE → Upload to GitHub |
| mlops-pipeline.yml | Commit → Test → Docs → Docker → Deploy to Minikube |
| ci-template.yml | Для GitHub Actions — автоматический деплой при пуше в main |
| edge-device.yml | Commit → Build EXE → Copy to Raspberry Pi via SCP |

СБОРКА И РЕЛИЗЫ — АВТОМАТИЗАЦИЯ ВСЕГО

Как собрать .exe и установщик?

```bash
pip install pyinstaller
pyinstaller --onefile --noconsole --icon=assets/icon.ico gui/main.py
upx --best dist/main.exe  # сжимаем
```

Как собрать Docker-образ?

```dockerfile
FROM python:3.11-slim
COPY . /app
WORKDIR /app
RUN pip install gitposter-core gitposter-action-* \
    && gitposter init --template=mlops
CMD ["gitposter", "run", "pipeline.yml"]
```

Как собрать установщик (.msi)?
- Используйте NSIS или Inno Setup через pyinstaller + cx_Freeze
- Генерируйте .msi автоматически в GitHub Actions:

```yaml
- name: Build Windows Installer
  run: |
    pip install cx_Freeze
    python setup.py bdist_msi
    cp dist/*.msi releases/
```

Как автоматически деплоить в K8s?
- Добавьте act_deploy_k8s.py → он использует kubectl
- Настройте KUBECONFIG через secret в GitHub Actions
- При пуше в main → автоматически деплоится в minikube или EKS

ПРОЦЕСС РАЗРАБОТКИ — ЦЕЛОСТНЫЙ ПАЙПЛАЙН

```
graph LR
    A[Разработка в GUI] --> B[Commit через GitPoster]
    B --> C[GitHub Actions запускает pipeline.yml]
    C --> D[Запуск тестов]
    D --> E[Генерация документации]
    E --> F[Сборка .exe]
    F --> G[Сборка Docker-образа]
    G --> H[Загрузка в GitHub Packages]
    H --> I[Деплой в Minikube/K8s]
    I --> J[Обновление README.md с диаграммой]
    J --> K[Создание GitHub Release]
    K --> L[Автоматическое уведомление Slack/Teams]
```

Всё это — один файл pipeline.yml.
Всё это — запускается из вашего GUI или из облака.

МЕТРИКИ УСПЕХА (для модуля M13)

| Метрика | Цель |
|--------|------|
| Количество действий (actions) | ≥ 8 |
| Покрытие тестами | ≥ 85% |
| Размер .exe | < 40 MB |
| Размер Docker-образа | < 300 MB |
| Время сборки пайплайна | < 90 сек (на GitHub Actions) |
| Документация | Все функции описаны, есть Mermaid-диаграммы |
| Возможность запуска в CI | Работает в GitHub Actions без Python |
| Поддержка OS | Windows, Linux, macOS |
# M15: Cloud-Native & Hybrid Architectures
Проблема:
Ваш продукт вырос. Вам нужна гео-распределённость, отказоустойчивость и выбор оптимального облака.

Инструменты:

Terraform, Crossplane, Istio (межоблачная сеть), Spinnaker, Kubernetes (EKS/GKE/AKS)

Практика:

Развернуть один сервис в Yandex Cloud, другой в AWS.

Настроить между ними шифрованный трафик через Istio.

Написать Terraform-модуль, который разворачивает всю инфраструктуру виртуального дата-центра (VPC, Subnets, K8s cluster, DB).

Реализовать blue-green деплой между разными облачными провайдерами.

Метрики успеха:

Zero-downtime деплой между облаками

Стоимость инфраструктуры оптимизирована (выбран правильный тип инстансов)

Задержка между сервисами в разных облаках < 50 мс


КАК ЭТО СВЯЗАНО С ВАШИМ ПУТЕМ EMAC?

| Модуль EMAC | Как связан с GitPoster SDK |
|-------------|----------------------------|
| M1 (C++) | Не нужен — но можно добавить act_compile_cpp.py для сборки C++-библиотек |
| M2 (Python Async) | GUI — на Qt, но ядро — асинхронное (asyncio) |
| M3 (Go) | Можно написать act_go_build.py — сборка Go-сервисов |
| M4 (Edge) | act_deploy_to_rpi.py — копирует .exe на Raspberry Pi |
| M5 (Docker) | act_build_docker.py — ядро |
| M6 (K8s) | act_deploy_k8s.py — ядро |
| M7 (MLOps) | act_gen_docs.py + act_run_tests.py — автоматизация ML-пайплайнов |
| M8 (CI/CD) | GitPoster — ваш CI-движок! |
| M9 (Observability) | Журнал действий → отправляется в Loki |
| M10 (Queues) | Можно добавить act_enqueue_job.py — ставит задачу в RabbitMQ |
| M11 (Frontend) | GUI — ваш фронтенд для DevOps |
| M12 (System Design) | Это — ваша система! Вы проектируете отказоустойчивую, распределённую, безопасную платформу |

GitPoster — это ваш ответ на вопрос: «Как сделать DevOps простым для технических специалистов, не умеющих писать команды?»

ПЛАН РАЗВИТИЯ: 6-МЕСЯЧНЫЙ ROADMAP

| Месяц | Цель |
|-------|------|
| М1 | Выпустить GitPoster SDK v0.1 — базовое ядро + 4 действия (commit, push, exe, docker) |
| М2 | Добавить тесты, DSL, CLI, документацию |
| М3 | Создать GitHub Actions-шаблон — чтобы любой мог запускать пайплайн |
| М4 | Добавить расширения: plugin-mlops, plugin-edge, plugin-unity |
| М5 | Собрать дистрибутив .exe + установщик + Docker-образ |
| М6 | Открыть репозиторий как open-source — опубликовать на PyPI, GitHub Marketplace |

ЗАКЛЮЧЕНИЕ: ВАШ ПУТЬ

| Уровень | Что вы получите |
|--------|----------------|
| Месяц 1–3 | Вы научитесь писать код, который работает в продакшене. |
| Месяц 4–6 | Вы научитесь проектировать системы, которые не падают. |
| Месяц 7–12 | Вы научитесь автоматизировать всё — от коммита до деплоя. |
| Месяц 13–18 | GIS. |
| Год 2 | Вы начинаете обучать других. Пишете статьи. Выступаете. |
| Год 3 | Вы — Tech Lead. Вас спрашивают: “Как нам сделать это правильно?” |