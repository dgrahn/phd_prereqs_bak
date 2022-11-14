# PhD Vulnerability Detection Prerequisites

## TODO
* Identify failure conditions for successful training. They should be fully learnable problems as there is zero noise.


## Results

Metric is binary accuracy, all datasets are balanced.

| # | Model       | Task 1    | Task 2    | Task 3    | Task 4    |
|---|-------------|-----------|-----------|-----------|-----------|
| 1 | Simple MLP  | 🟢 0.9968 | 🟢 0.9968 | 🔴 0.5068 | 🔴 0.5080 |
| 2 | CNN + MLP   | 🟢 0.9965 | 🟢 0.9952 | 🔴 0.5068 | 🔴 0.5080 |
| 3 | LSTM + MLP  | 🟢 0.9938 | 🔴 0.5027 | 🔴 0.5068 | 🔴 0.5080 |
| 4 | Transformer | ⚪ 0.xxxx | ⚪ 0.xxxx | ⚪ 0.xxxx | ⚪ 0.xxxx |
| 5 | GNN         | ⚪ 0.xxxx | ⚪ 0.xxxx | ⚪ 0.xxxx | ⚪ 0.xxxx |

### Legend
* 🟢 >= 0.95
* 🟡 >= 0.80
* 🟠 ~> 0.50
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


