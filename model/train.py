from typing import Callable

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import torch
import torch.nn as nn
from torch.nn.modules.loss import _Loss as Criterion
from torch.optim.optimizer import Optimizer
from torch.utils.data import DataLoader
from tqdm import tqdm


def train_net(
    net: nn.Module,
    train_data_loader: DataLoader,
    eval_data_loader: DataLoader,
    optimizer: Optimizer,
    criterion: Criterion,
    eval_fn: Callable,
    epochs: int,
    device: str,
    logger=None,
    verbose: bool = True,
):
    net.train()
    net.to(device)

    rng = range(epochs)
    if verbose:
        rng = tqdm(rng)

    for epoch in rng:
        running_loss = 0.0
        for x, y in train_data_loader:
            x, y = x.to(device), y.to(device)
            optimizer.zero_grad()
            preds = net(x)
            loss = criterion(preds, y)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
        train_loss = running_loss / len(train_data_loader)
        eval = eval_fn(net, eval_data_loader, device)
        if logger:
            logger.add_scalar("train_loss", train_loss, epoch)
            logger.add_scalar("eval", eval, epoch)
            logger.info(
                f"Epoch {epoch + 1}/{epochs}, Train Loss: {train_loss}, Evaluation: {eval}"
            )
        if verbose:
            print(
                f"Epoch {epoch + 1}/{epochs}, Train Loss: {train_loss}, Evaluation: {eval}"
            )
        yield train_loss, eval


def get_mae(net: nn.Module, data_loader: DataLoader, device: str):
    net.eval()
    mae = 0.0
    with torch.no_grad():
        for (
            x,
            y,
        ) in data_loader:
            x, y = x.to(device), y.to(device)
            preds = net(x)
            mae += torch.abs(preds - y).sum().item()
    net.train()
    return mae / len(data_loader)


def get_accuracy(net: nn.Module, data_loader: DataLoader, device: str):
    net.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for (
            x,
            y,
        ) in data_loader:
            x, y = x.to(device).unsqueeze(2), y.to(device)
            preds = net(x)
            _, predicted = torch.max(preds, 1)
            total += y.size(0)
            correct += (predicted == y).sum().item()
    net.train()
    return correct / total


def get_confusion_matrix(
    net: nn.Module, data_loader: DataLoader, n_classes: int, device: str
):
    net.eval()
    confusion_matrix = torch.zeros(n_classes, n_classes)
    with torch.no_grad():
        for (
            x,
            y,
        ) in data_loader:
            x, y = x.to(device), y.to(device)
            preds = net(x)
            _, predicted = torch.max(preds, 1)
            for t, p in zip(y.view(-1), predicted.view(-1)):
                confusion_matrix[t.long(), p.long()] += 1
    net.train()
    return confusion_matrix


def get_f1_score(net: nn.Module, data_loader: DataLoader, n_classes: int, device: str):
    net.eval()
    confusion_matrix = torch.zeros(n_classes, n_classes)
    with torch.no_grad():
        for x, y in data_loader:
            x, y = x.to(device), y.to(device)
            preds = net(x)
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
