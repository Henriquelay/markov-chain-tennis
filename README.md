# Markov-chain-tennis

Generates and analyse tennis matches to study Markov chains.

## Getting Started

### Dependencies

#### Dataset generator (`tennis.py`)

* Python 3.10

#### Analysis (`grapher.ipynb`)

* Python 3.10
* Jupyter 7.1

### Installing

#### Analysis

Install `requirements.txt` with your favorite virtual environment.

```shell
pip install -r requirements.txt
```

With pip, or use your virtual environment's equivalent.

### Executing program

```shell
python tennis.py <advantage chance> <fair chance> --runs <number of runs>
```

Example

```shell
python tennis.py 0.7 0.45 --runs 200
```

## License

This project is licensed under the [GPLv2] License - see the LICENSE file for details
