"""Відтворення навчального експерименту ЛР9 (без власної velocity)."""
from pathlib import Path
import csv
import math
import random

DATA = Path(__file__).resolve().parent / "lr09_reference_velocity.csv"


def simulate(velocity, points=220, runs=10000, seed=20261109):
    if not velocity or any(v < 0 for v in velocity) or max(velocity) == 0:
        raise ValueError("Очікується непорожня вибірка з невід’ємною velocity та хоча б одним додатним значенням")
    rng = random.Random(seed)
    results = []
    for _ in range(runs):
        remaining = points
        sprints = 0
        while remaining > 0:
            remaining -= rng.choice(velocity)
            sprints += 1
        results.append(sprints)
    results.sort()
    p50 = results[math.ceil(runs * 0.50) - 1]
    p85 = results[math.ceil(runs * 0.85) - 1]
    return p50, p85


with DATA.open(encoding="utf-8-sig", newline="") as file:
    values = [int(row["points_done"]) for row in csv.DictReader(file)]

for name, sample in (
    ("Усі 12 навчальних спринтів", values),
    ("Навчальні спринти 1 і 2", values[:2]),
    ("Навчальні спринти 5 і 6", values[4:6]),
):
    p50, p85 = simulate(sample)
    print(f"{name}: P50={p50}, P85={p85}")
