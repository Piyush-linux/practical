# Adaptive Resonance Theory (ART-1)
# For binary input patterns

import numpy as np

# Parameters
vigilance = 0.7  # Vigilance parameter (ρ)
learning_rate = 1.0  # Learning rate

# Input patterns (binary)
patterns = np.array([[1, 1, 0, 0], [1, 0, 0, 0], [0, 0, 1, 1], [0, 0, 1, 0]])

num_patterns, num_features = patterns.shape

# Initialize weights
weights = []


def similarity(p, w):
    return np.sum(np.minimum(p, w)) / np.sum(p)


print("Adaptive Resonance Theory (ART-1)\n")

for idx, pattern in enumerate(patterns):
    print(f"Input pattern {idx + 1}: {pattern}")
    matched = False

    for j, w in enumerate(weights):
        sim = similarity(pattern, w)

        if sim >= vigilance:
            print(f" → Resonates with category {j + 1}")
            # Update weights
            weights[j] = np.minimum(w, pattern)
            matched = True
            break

    if not matched:
        print(" → Creating new category")
        weights.append(pattern.copy())

    print()

print("Final learned categories:")
for i, w in enumerate(weights):
    print(f"Category {i + 1}: {w}")
