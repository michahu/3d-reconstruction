# X:
# 1. Compute PCA of point cloud -> take 3 resultant vectors -> R9
# 2. Categorize cameras radially -> R16
# Concatenate vectors into R25

# Y:
# 1 hot encoding of where next minimal camera should be

# Loss:
# Cross Entropy

# Neural network architecture: 1 hidden layer
# R25 -> R20 -> R16

# Other approaches to consider:
# SVM, Random Forest

# Following code is adapted from https://pytorch.org/tutorials/beginner/blitz/cifar10_tutorial.html

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np
import sys
import os

class CameraClassifier(nn.Module):
    def __init__(self):
        super().__init__()
        self.hidden = nn.Linear(25, 20)
        self.output = nn.Linear(20, 16)

    def forward(self, x):
        x = F.relu(self.hidden(x))
        x = F.softmax(self.output(x), dim=-1).unsqueeze(0)
        return x

def main(file, checkpoint):
    net = CameraClassifier()
    if os.path.exists(checkpoint):
        net.load_state_dict(torch.load(checkpoint))

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.9)

    # doesn't exist yet
    # training_data = np.load('data.npz')['training_data']
    training_data = np.load(file)

    for epoch in range(10):
        running_loss = 0.0
        for i, (inputs, labels) in enumerate(zip(training_data['x'], training_data['y'])):
            # zero the parameter gradients
            inputs = torch.Tensor(inputs)
            labels = torch.LongTensor([labels])

            optimizer.zero_grad()

            # forward + backward + optimize
            outputs = net(inputs)
            # print(outputs.shape)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            # print statistics
            running_loss += loss.item()
            if i % 10 == 9:    # print every 100 mini-batches
                print('[%d, %5d] loss: %.3f' %
                        (epoch + 1, i + 1, running_loss / 10))
                running_loss = 0.0

    torch.save(net.state_dict(), 'checkpoint')

    print('Finished Training')

if __name__ == '__main__':
    if len(sys.argv) < 3:
      print("Usage: python nn.py <training_data.npz> <checkpoint>")
      exit()
    main(sys.argv[1], sys.argv[2])
