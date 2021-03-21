# timer

## How to use
```bash
git clone git@github.com:lucasrcezimbra/timer.git
cd timer
python timer.py -- [COMMAND AND ARGS ...]
```

## How to develop
```bash
git clone git@github.com:lucasrcezimbra/timer.git
cd timer
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pre-commit install
pytest
```
