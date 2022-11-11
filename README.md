# PhD Vulnerability Detection Prerequisites


## Results

FIXME: Where are the failure conditions???


| Model       | Task 1    | Task 2    | Task 3    | Task 4    |
|-------------|-----------|-----------|-----------|-----------|
| Simple MLP  | ⚪ 0.xxxx | ⚪ 0.xxxx | ⚪ 0.xxxx | ⚪ 0.xxxx |
| CNN + MLP   | ⚪ 0.xxxx | ⚪ 0.xxxx | ⚪ 0.xxxx | ⚪ 0.xxxx |
| LSTM + MLP  | ⚪ 0.xxxx | ⚪ 0.xxxx | ⚪ 0.xxxx | ⚪ 0.xxxx |
| Transformer | ⚪ 0.xxxx | ⚪ 0.xxxx | ⚪ 0.xxxx | ⚪ 0.xxxx |
| GNN         | ⚪ 0.xxxx | ⚪ 0.xxxx | ⚪ 0.xxxx | ⚪ 0.xxxx |

### Legend
* 🟢 > 0.95
* 🟡 > 0.80
* 🟠 > 0.50
* 🔴 = 0.50
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


