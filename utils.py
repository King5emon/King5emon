# utils.py — helper math functions for your forex-ai app

import numpy as np


def calc_trend(prices):
    """Simple linear regression slope to detect trend direction."""
    if len(prices) < 2:
        return 0
    x = np.arange(len(prices))
    y = np.array(prices)
    slope = np.polyfit(x, y, 1)[0]
    return slope


def classify_trend(slope):
    """Interpret slope into BUY or SELL bias."""
    if slope > 0:
        return "BUY BIAS (Uptrend)"
    elif slope < 0:
        return "SELL BIAS (Downtrend)"
    return "SIDEWAYS (No clear trend)"


def normalize(v):
    """Normalize a vector."""
    n = np.linalg.norm(v)
    if n == 0:
        return v
    return v / n


def distance(p1, p2):
    """Euclidean distance between 2 points."""
    return float(np.linalg.norm(np.array(p1) - np.array(p2)))


def midprice(high, low):
    """Fair middle price."""
    return (high + low) / 2


def detect_liquidity_levels(prices, sensitivity=0.7):
    """
    Finds swing highs/lows (liquidity zones).
    Very simple heuristic.
    """
    if len(prices) < 5:
        return [], []

    highs = []
    lows = []

    for i in range(2, len(prices) - 2):
        window = prices[i - 2:i + 3]
        center = prices[i]

        if center == max(window) and center > np.mean(window) * (1 + sensitivity * 0.01):
            highs.append((i, center))

        if center == min(window) and center < np.mean(window) * (1 - sensitivity * 0.01):
            lows.append((i, center))

    return highs, lows
