# PhD Vulnerability Detection Prerequisites

## TODO
* Identify failure conditions for successful training. They should be fully learnable problems as there is zero noise.
* Try training CodeBERT with no frozen weights (running on fry now)
* Simplify code


## Results

Metric is binary accuracy, all datasets are balanced.

| # | Model       | Task 1    | Task 2     | Task 3    | Task 4     | Task 5    |
|---|-------------|-----------|------------|-----------|------------|-----------|
| 1 | Simple MLP  | 🟢 0.9967 | 🟢 0.9955 | 🔴 0.5068 | 🔴 0.5080 | 🟡 0.5375 |
| 2 | CNN + MLP   | 🟢 0.9970 | 🔴 0.5052 | 🔴 0.5068 | 🔴 0.5080 | 🔴 0.5027 |
| 3 | LSTM + MLP  | 🟢 0.9936 | 🔴 0.5052 | 🔴 0.5068 | 🔴 0.5080 | 🔴 0.5027 |
| 4 | CodeBERT    | ⚪ 0.5052 | ⚪ 0.5054 | ⚪ 0.5067 | ⚪ 0.xxxx | ⚪ 0.xxxx |
| 5 | GNN         | 🟢 0.9288 | 🟡 0.7259 | 🔴 0.5038 | 🔴 0.5026 | 🟡 0.5365 |

### Legend
* 🟢 >= 0.90
* 🟡 ~> 0.50
* 🔴 ~= 0.50 (Due to size of sample, may not be exactly 0.5000)
* ⚪ Untested


### Training Info
#### Simple MLP
| Property         | Value               |
|------------------|---------------------|
| Optimizer        | Adam                |
| Loss             | Binary Crossentropy |
| Epochs           | 10                  |
| Steps per Epoch  | 10,000              |
| Validation Steps | 1,000               |

1. Simple MLP
2. CNN + MLP (commonly used in MLAVD)
3. RNN (probably an LSTM for efficiency)
4. Transformer (BERT-style)
5. GNN


## Notes
* The modulo operator for python and C++ work differently for negative numbers. Because the exact operation of the modulo isn't issue, but being able to evaluate it I've decided to ignore the difference.
* Not Supported
    * Assignment Operators (+=, -=, etc.)
    * Increment/decrement (++, --)


