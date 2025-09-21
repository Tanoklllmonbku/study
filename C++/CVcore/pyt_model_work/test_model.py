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