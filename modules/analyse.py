import torch
from PIL import Image
import torchvision.transforms as transforms
from torchvision.transforms import ToTensor
import matplotlib.pyplot as plt
from modules import DigitNetwork

model = DigitNetwork.MNISTModule()
device = torch.accelerator.current_accelerator().type if torch.accelerator.is_available() else "cpu"

try:
    model.load_state_dict(torch.load("mnist_digit_model.pth"))
except Exception as e:
    print("Could not load Model Training:", e)

model.eval()

def analyseImage():

    image = Image.open("cDraw.png")

    transform = transforms.Compose([
        transforms.Grayscale(num_output_channels=1),
        transforms.Resize((28, 28)),
        transforms.ToTensor(),
    ])

    bbox = image.getbbox()

    if bbox is None:
        print("No drawing found.")
        return

    image = image.crop(bbox)
    image.thumbnail((20, 20), Image.Resampling.LANCZOS)

    final_image = Image.new("L", (28, 28), 0)

    x_offset = (28 - image.width) // 2
    y_offset = (28 - image.height) // 2

    final_image.paste(image, (x_offset, y_offset))

    transform = transforms.ToTensor()
    image_tensor = transform(final_image).unsqueeze(0)

    print("Tensor Shape:", image_tensor.shape)

    print("Analysis from file")
    with torch.no_grad():
        prediction = model(image_tensor)
        probabilities = torch.softmax(prediction, dim=1)
        predicted_num = probabilities.argmax(dim=1).item()

    print(predicted_num)

    for digit, confidence in enumerate(probabilities[0]):
        print(f"{digit}: {confidence.item():.2%}")

    plt.imshow(image, cmap="gray")
    plt.title(f"Predicted: {predicted_num}")
    plt.show()

