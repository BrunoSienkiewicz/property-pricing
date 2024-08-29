import torch
import torch.nn as nn
import matplotlib.pyplot as plt
import seaborn as sns   
import numpy as np
from torch.nn.utils.rnn import pad_sequence 
from tqdm import tqdm


def train_net(net, train_data_loader, eval_data_loader, optimizer, criterion, eval_fn, epochs, device, logger=None):
    net.train()
    net.to(device)

    for epoch in range(epochs):
        running_loss = 0.0
        for x, y in tqdm(train_data_loader):
            x, y = x.to(device).unsqueeze(2), y.to(device)
            optimizer.zero_grad()
            preds, _ = net(x)
            loss = criterion(preds, y)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
        train_loss = running_loss / len(train_data_loader)
        eval = eval_fn(net, eval_data_loader, device)
        if logger:
            logger.add_scalar('train_loss', train_loss, epoch)
            logger.add_scalar('eval', eval, epoch)
            logger.info(f'Epoch {epoch + 1}/{epochs}, Train Loss: {train_loss}, Evaluation: {eval}')
        else:
            print(f'Epoch {epoch + 1}/{epochs}, Train Loss: {train_loss}, Evaluation: {eval}')
            yield train_loss, eval


def get_accuracy(net, data_loader, device):
    net.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for x, y, in data_loader:
            x, y = x.to(device).unsqueeze(2), y.to(device)
            preds, _ = net(x)
            _, predicted = torch.max(preds, 1)
            total += y.size(0)
            correct += (predicted == y).sum().item()
    net.train()
    return correct / total


def get_confusion_matrix(net, data_loader, n_classes, device):
    net.eval()
    confusion_matrix = torch.zeros(n_classes, n_classes)
    with torch.no_grad():
        for x, y, in data_loader:
            x, y = x.to(device), y.to(device)
            preds, _ = net(x)
            _, predicted = torch.max(preds, 1)
            for t, p in zip(y.view(-1), predicted.view(-1)):
                confusion_matrix[t.long(), p.long()] += 1
    net.train()
    return confusion_matrix


def get_f1_score(net, data_loader, n_classes, device):
    net.eval()
    confusion_matrix = torch.zeros(n_classes, n_classes)
    with torch.no_grad():
        for x, y in data_loader:
            x, y = x.to(device), y.to(device)
            preds, _ = net(x)
            _, predicted = torch.max(preds, 1)
            for t, p in zip(y.view(-1), predicted.view(-1)):
                confusion_matrix[t.long(), p.long()] += 1
    net.train()
    TP = confusion_matrix.diag()
    FP = confusion_matrix.sum(dim=0) - TP
    FN = confusion_matrix.sum(dim=1) - TP
    TN = confusion_matrix.sum() - (TP + FP + FN)
    precision = TP / (TP + FP)
    recall = TP / (TP + FN)
    f1 = 2 * (precision * recall) / (precision + recall)
    return f1.mean().item()

