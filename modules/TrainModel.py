import DigitNetwork

import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets
from torchvision.transforms import ToTensor
import matplotlib.pyplot as plt

model = DigitNetwork.MNISTModule()
print(model)

training_data = datasets.MNIST(
    root="data",
    train=True,
    download=True,
    transform=ToTensor()
)

test_data = datasets.MNIST(
    root="data",
    train=False,
    download=True,
    transform=ToTensor()
)

batch_size = 64

train_loader = DataLoader(training_data, batch_size=batch_size, shuffle=True)
test_loader = DataLoader(test_data, batch_size=batch_size, shuffle=False)

images, labels = next(iter(train_loader))

loss_function = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

epochs = 10

for e in range(epochs):
    print(f"\nEpoch {e + 1}")
    model.train()

    tLoss = 0

    for batch, (images, labels) in enumerate(train_loader):
        # Make Predictions
        predictions = model(images)

        # Calculate error margin
        loss = loss_function(predictions, labels)

        # Reset old gradients
        optimizer.zero_grad()

        # Backpropogation
        loss.backward()

        # Update Weights
        optimizer.step()

        tLoss += loss.item()

        if batch % 100 == 0:
            print(f"Batch {batch}, Loss: {loss.item():.4f}")

    avgLoss = tLoss / len(train_loader)
    print(f"Avg Loss: {avgLoss:.4f}")

try:
    torch.save(model.state_dict(), "mnist_digit_model.pth")
    print("Saved Model Training!")
except Exception as e:
    print("Unable to save model training:", e)



# Accuracy Check

# model.eval()

# correct = 0
# total = 0

# with torch.no_grad():
#     for images, labels in test_loader:
#         preds = model(images)

#         predictedDigits = preds.argmax(dim=1)

#         correct += (predictedDigits == labels).sum().item()
#         total += labels.size(0)

# accuracy = correct / total
# print(f"Test Accuracy: {accuracy:.2%}")

# image, label = test_data[0]

# model.eval()

# with torch.no_grad():
#     pred = model(image.unsqueeze(0))
#     predDigit = pred.argmax(dim=1).item()

# plt.imshow(image.squeeze(), cmap="gray")
# plt.title(f"Actual: {label}, Predicted: {predDigit}")
# plt.show()