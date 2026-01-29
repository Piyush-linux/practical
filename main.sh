#!/usr/bin/env bash

set -e

BASE_URL="https://raw.githubusercontent.com/Piyush-linux/practical/master"
echo $BASE_URL
TOPICS=(
  "lnnm.py" # Design a simple linear neural network model
  "bbsf.py" # Calculate the output of neural net using both binary and bipolar sigmoidal function
  "mpAnd.py" # Generate AND/NOT function using McCulloch-Pitts neural net
  "mpnn.py" # Generate XOR function using McCulloch-Pitts neural net
  "hr.py" # Write a program to implement Hebb’s rule
  "dr.py" # Write a program to implement of delta rule
  "bpa.py" # Write a program for Back Propagation Algorithm
  "eba.py" # Write a program for error Backpropagation algorithm
  "hn.py" # Write a program for Hopfield Network
  "rbf.py" # Write a program for Radial Basis function
  "kso.py" # Kohonen Self organizing map
  "art.py" # Adaptive resonance theory
  "ls.py" # Write a program for Linear separation
  "hnm.py" # Write a program for Hopfield network model for associative memory
  "io_in.py" # Membership and Identity Operators | in, not in
  "io_is.py" # Membership and Identity Operators is, is not
  "fl.py" # Find ratios using fuzzy logic
  "fl_t.py" # Solve Tipping problem using fuzzy logic
  "sga.py" # Implementation of Simple genetic algorithm
  "ga.py" # Create two classes: City and Fitness using Genetic algorithm
)

echo "📦 Available topics:"
echo "---------------------"

for i in "${!TOPICS[@]}"; do
  printf "%d) %s\n" "$((i+1))" "${TOPICS[$i]}"
done

echo
read -p "Select a topic (number): " choice

INDEX=$((choice-1))

if [[ -z "${TOPICS[$INDEX]}" ]]; then
  echo "❌ Invalid selection"
  exit 1
fi

FILE="${TOPICS[$INDEX]}"
URL="$BASE_URL/code/$FILE"
echo $URL
echo "⬇️  Downloading: $FILE"
curl -fsSL "$URL" -o "$FILE"

# chmod +x "$FILE"

# echo "✅ Done"
# echo "👉 Run with: ./$FILE"
