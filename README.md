# Alpaca

## Quick start

```
conda create -n alpaca
conda activate alpaca
brew install cmake # only for mac
brew install pkg-config # only for mac
pip install -r requirements.txt
cd ~/miniconda3/envs/alpaca/lib/python3.11/site-packages/bitsandbytes/
cp libbitsandbytes_cuda114.so libbitsandbytes_cpu.so
```