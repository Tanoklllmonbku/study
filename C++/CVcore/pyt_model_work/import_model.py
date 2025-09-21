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