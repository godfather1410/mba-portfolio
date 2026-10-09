"""Network: a pretrained ResNet-18 backbone with two classification heads.

The original project hand-wrote an Inception-v3 in TFLearn and trained it from
scratch to output one of 9 key combos. Here:
  * ResNet-18 pretrained on ImageNet (already knows edges/shapes -> needs far
    less driving data than training from scratch).
  * Two heads (steer: L/S/R, throttle: brake/coast/accelerate) instead of one
    9-way head, so the model doesn't have to learn every combination separately.
  * Optional speed input (from Forza telemetry) concatenated to the image features.
"""
import torch
import torch.nn as nn

import config


def build_model(pretrained=True, use_speed=False):
    import torchvision
    weights = torchvision.models.ResNet18_Weights.DEFAULT if pretrained else None
    try:
        backbone = torchvision.models.resnet18(weights=weights)
    except Exception as e:  # noqa: BLE001 - e.g. no internet to fetch weights
        print(f"[model] could not load pretrained weights ({e}); training from scratch")
        backbone = torchvision.models.resnet18(weights=None)
    feat = backbone.fc.in_features
    backbone.fc = nn.Identity()
    return DrivingNet(backbone, feat, use_speed)


class DrivingNet(nn.Module):
    def __init__(self, backbone, feat, use_speed):
        super().__init__()
        self.backbone = backbone
        self.use_speed = use_speed
        extra = 1 if use_speed else 0
        self.trunk = nn.Sequential(nn.Linear(feat + extra, 128), nn.ReLU(), nn.Dropout(0.3))
        self.steer_head = nn.Linear(128, config.N_STEER)
        self.thr_head = nn.Linear(128, config.N_THROTTLE)

    def forward(self, x, speed=None):
        f = self.backbone(x)
        if self.use_speed:
            f = torch.cat([f, speed.unsqueeze(1) / 50.0], dim=1)  # ~m/s scaled to ~0..1
        h = self.trunk(f)
        return self.steer_head(h), self.thr_head(h)
