# prints test accuracy on test set

from nn import CameraClassifier
import torch
import numpy as np

model = CameraClassifier()
model.load_state_dict(torch.load('checkpoint'))
model.eval() # sets model to evaluation mode

test_data = np.load('data.npz')['test_data']

correct = 0
total = 0
with torch.no_grad():
    for data in test_data:
        inputs, labels = data
        outputs = model(inputs)
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

print('Accuracy of the network on the 10000 test images: %d %%' % (
    100 * correct / total))


