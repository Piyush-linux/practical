#!/usr/bin/env python3
"""
hopfield_demo.py

Simple Hopfield network demo (binary / bipolar {-1,+1} neurons).
- Creates patterns (checkerboard + random)
- Stores them using Hebbian rule (outer-product)
- Initializes network with a noisy pattern
- Runs synchronous updates and monitors states & overlaps
- Plots patterns, overlap matrix, and state sequence

Author: assistant (cleaned and packaged)
"""

from typing import List, Tuple

import matplotlib.pyplot as plt
import numpy as np

np.random.seed(1)


class PatternFactory:
    def __init__(self, shape: Tuple[int, int]):
        self.shape = shape
        self.N = shape[0] * shape[1]

    def create_checkerboard(self) -> np.ndarray:
        rows, cols = self.shape
        patt = np.zeros((rows, cols), dtype=int)
        for r in range(rows):
            for c in range(cols):
                patt[r, c] = 1 if (r + c) % 2 == 0 else -1
        return patt

    def create_random_pattern(self, on_probability: float = 0.5) -> np.ndarray:
        rows, cols = self.shape
        # map True -> +1, False -> -1
        rand = np.random.rand(rows, cols) < on_probability
        patt = np.where(rand, 1, -1).astype(int)
        return patt

    def create_random_pattern_list(
        self, nr_patterns: int, on_probability: float = 0.5
    ) -> List[np.ndarray]:
        return [self.create_random_pattern(on_probability) for _ in range(nr_patterns)]

    def reshape_patterns(self, patterns_flat: np.ndarray) -> List[np.ndarray]:
        """Convert array of shape (steps, N) to list of (rows,cols) patterns."""
        return [p.reshape(self.shape) for p in patterns_flat]


class PatternTools:
    @staticmethod
    def flatten(pattern: np.ndarray) -> np.ndarray:
        return pattern.flatten()

    @staticmethod
    def flip_n(pattern: np.ndarray, nr_of_flips: int) -> np.ndarray:
        """Return a new pattern with exactly nr_of_flips bits flipped (bipolar)."""
        flat = pattern.flatten().copy()
        n = flat.size
        flip_idx = np.random.choice(n, size=min(nr_of_flips, n), replace=False)
        flat[flip_idx] *= -1
        return flat.reshape(pattern.shape)

    @staticmethod
    def compute_overlap(p1: np.ndarray, p2: np.ndarray) -> float:
        """Normalized overlap between two bipolar patterns in [-1,+1].
        overlap = (1/N) * sum_i p1_i * p2_i
        """
        a = p1.flatten()
        b = p2.flatten()
        return float(np.dot(a, b) / a.size)

    @staticmethod
    def compute_overlap_matrix(pattern_list: List[np.ndarray]) -> np.ndarray:
        K = len(pattern_list)
        M = np.zeros((K, K), dtype=float)
        for i in range(K):
            for j in range(K):
                M[i, j] = PatternTools.compute_overlap(pattern_list[i], pattern_list[j])
        return M


class HopfieldNetwork:
    def __init__(self, N: int):
        self.N = N
        self.W = np.zeros((N, N), dtype=float)  # weights
        self.state = np.ones(N, dtype=int)  # current network state, bipolar {-1,+1}

    def store_patterns(self, patterns: List[np.ndarray]):
        """Hebbian storage: w = sum_p (p p^T) with zero diagonal."""
        self.W.fill(0.0)
        for patt in patterns:
            v = PatternTools.flatten(patt).astype(float)
            self.W += np.outer(v, v)
        # zero diagonal (no self-connection)
        np.fill_diagonal(self.W, 0.0)
        # Optionally normalize by number of neurons (not required)
        # self.W /= self.N

    def set_state_from_pattern(self, pattern: np.ndarray):
        self.state = PatternTools.flatten(pattern).astype(int).copy()

    def run_with_monitoring(
        self, nr_steps: int, deterministic: bool = True
    ) -> np.ndarray:
        """Run synchronous dynamics, return array of states (nr_steps+1 x N) including initial."""
        states = np.zeros((nr_steps + 1, self.N), dtype=int)
        states[0, :] = self.state.copy()
        s = self.state.copy()
        for t in range(1, nr_steps + 1):
            h = self.W.dot(s)  # input potentials
            if deterministic:
                # sign function: for zero field, keep previous value
                s_new = np.where(h > 0, 1, np.where(h < 0, -1, s))
            else:
                # stochastic update using sigmoid probability g(h) = 0.5*(1 + tanh(beta*h))
                beta = 1.0
                probs = 0.5 * (1 + np.tanh(beta * h))
                draws = np.random.rand(self.N)
                s_new = np.where(draws < probs, 1, -1)
            s = s_new
            states[t, :] = s
        self.state = s
        return states


class PlotTools:
    @staticmethod
    def plot_pattern_list(pattern_list: List[np.ndarray], suptitle: str = "Patterns"):
        k = len(pattern_list)
        cols = min(6, k)
        rows = (k + cols - 1) // cols
        plt.figure(figsize=(cols * 2, rows * 2))
        for i, patt in enumerate(pattern_list):
            plt.subplot(rows, cols, i + 1)
            plt.imshow(patt, cmap="gray", vmin=-1, vmax=1)
            plt.title(f"P{i}")
            plt.axis("off")
        plt.suptitle(suptitle)
        plt.show()

    @staticmethod
    def plot_overlap_matrix(M: np.ndarray):
        plt.figure(figsize=(5, 4))
        plt.imshow(M, cmap="bwr", vmin=-1, vmax=1)
        plt.colorbar(label="overlap")
        plt.title("Overlap matrix")
        plt.xlabel("pattern j")
        plt.ylabel("pattern i")
        plt.show()

    @staticmethod
    def plot_state_sequence_and_overlap(
        states_as_patterns: List[np.ndarray],
        pattern_list: List[np.ndarray],
        reference_idx: int = 0,
        suptitle: str = "",
    ):
        # plot each state
        k = len(states_as_patterns)
        cols = k
        rows = 1
        plt.figure(figsize=(cols * 2.2, 3))
        for i, patt in enumerate(states_as_patterns):
            plt.subplot(1, cols, i + 1)
            plt.imshow(patt, cmap="gray", vmin=-1, vmax=1)
            plt.title(f"t={i}")
            plt.axis("off")
        plt.suptitle(suptitle)
        plt.show()

        # overlaps between each state and reference pattern
        ref = pattern_list[reference_idx]
        overlaps = [
            PatternTools.compute_overlap(state, ref) for state in states_as_patterns
        ]
        plt.figure(figsize=(6, 3))
        plt.plot(overlaps, marker="o")
        plt.ylim(-1.05, 1.05)
        plt.xlabel("time step")
        plt.ylabel("overlap with reference")
        plt.title("Overlap over time")
        plt.grid(True)
        plt.show()


def demo():
    # configuration
    shape = (6, 6)  # pattern grid
    factory = PatternFactory(shape)
    # create patterns
    checkerboard = factory.create_checkerboard()
    random_patterns = factory.create_random_pattern_list(
        nr_patterns=3, on_probability=0.5
    )
    pattern_list = [checkerboard] + random_patterns

    # plotting patterns
    PlotTools.plot_pattern_list(pattern_list, suptitle="Stored patterns")

    # compute overlap matrix
    overlap_matrix = PatternTools.compute_overlap_matrix(pattern_list)
    print("Overlap matrix:\n", overlap_matrix)
    PlotTools.plot_overlap_matrix(overlap_matrix)

    # store patterns in network
    hop = HopfieldNetwork(N=shape[0] * shape[1])
    hop.store_patterns(pattern_list)

    # create noisy initialization from checkerboard
    noisy_init = PatternTools.flip_n(checkerboard, nr_of_flips=8)
    hop.set_state_from_pattern(noisy_init)
    print(
        "Initial overlap with checkerboard:",
        PatternTools.compute_overlap(noisy_init, checkerboard),
    )

    # run dynamics for a few steps and monitor
    states = hop.run_with_monitoring(nr_steps=6)
    states_as_patterns = factory.reshape_patterns(states)
    PlotTools.plot_state_sequence_and_overlap(
        states_as_patterns,
        pattern_list,
        reference_idx=0,
        suptitle="Network dynamics (synchronous updates)",
    )

    # final state overlap
    final_overlap = PatternTools.compute_overlap(states_as_patterns[-1], checkerboard)
    print("Final overlap with checkerboard:", final_overlap)


if __name__ == "__main__":
    demo()
