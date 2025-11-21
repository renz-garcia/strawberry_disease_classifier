import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import models
from torchmetrics.classification import Accuracy, Precision, Recall, F1Score, AUROC

class ResNet50(nn.Module):
    def __init__(self, num_classes=2, freeze_backbone=True, gamma=2.5, alpha=0.75, device='cpu'):
        super(ResNet50, self).__init__()

        # Load pretrained ResNet-50
        self.model = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V2)

        # Freeze backbone if specified
        if freeze_backbone:
            for param in self.model.parameters():
                param.requires_grad = False

        # Replace classifier head for binary classification
        in_features = self.model.fc.in_features
        self.model.fc = nn.Sequential(
            nn.Linear(in_features, 512),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(512, 1),
        )

        # Hyperparameters
        self.gamma = gamma
        self.alpha = alpha
        self.device = device

        # TorchMetrics for binary classification
        self.accuracy = Accuracy(task="binary").to(device)
        self.precision = Precision(task="binary").to(device)
        self.recall = Recall(task="binary").to(device)
        self.f1 = F1Score(task="binary").to(device)
        self.auroc = AUROC(task="binary").to(device)

    def forward(self, x):
        return self.model(x)

    def focal_loss(self, outputs, targets):
        bce_loss = F.binary_cross_entropy_with_logits(outputs, targets.float(), reduction="none")
        probs = torch.sigmoid(outputs)
        pt = torch.where(targets == 1, probs, 1 - probs)
        focal_weight = (1 - pt) ** self.gamma
        loss = self.alpha * focal_weight * bce_loss
        return loss.mean()

    def get_loss_function(self):
        return self.focal_loss

    def compute_metrics(self, outputs, targets):
        preds = (torch.sigmoid(outputs) > 0.4).long().squeeze()
        metrics = {
            "accuracy": self.accuracy(preds, targets).item(),
            "precision": self.precision(preds, targets).item(),
            "recall": self.recall(preds, targets).item(),
            "f1": self.f1(preds, targets).item(),
            "auroc": self.auroc(torch.sigmoid(outputs), targets).item()
        }
        return metrics