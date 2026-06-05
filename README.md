# Blockchain

A minimal Python blockchain implementation that demonstrates block hashing, chain validation, and proof-of-work mining at varying difficulty levels.

## Overview

This project is an educational, from-scratch implementation of the core mechanics behind a blockchain. Blocks are stored as nodes in a linked list, each linked to its predecessor by a SHA-256 hash. The chain can be validated, tampered with, and mined against a configurable difficulty target.

## Features

- **SHA-256 block hashing** over payload, timestamp, previous hash, index, and nonce
- **Linked-list chain structure** via custom `Node` and `Block` classes
- **Chain validation** that detects tampering of any block
- **Sabotage method** to demonstrate how altering a block invalidates the chain
- **Proof-of-work mining** with adjustable difficulty (leading-zero hash target)

## Project Structure

```
Blockchain/
├── Block.py        # Block data structure (payload, hashes, nonce, index)
├── Node.py         # Linked-list node wrapping a Block
├── Blockchain.py   # Chain logic: add, validate, sabotage, mine
└── Main.py         # Example usage and mining benchmark
```

## Requirements

- Python 3.x (no external dependencies — uses only the standard library)

## Usage

Run the example:

```bash
python Main.py
```

### Building a chain

```python
from Blockchain import Blockchain

bc = Blockchain()
bc.addBlock("hallo")
bc.addBlock("das")
bc.addBlock("ist")
bc.addBlock("ein")
bc.addBlock("test")

bc.printBlockchain()
print(bc.isValid())   # True
```

### Detecting tampering

```python
bc.sabotage(1, "other")
print(bc.isValid())   # False
```

### Mining with proof-of-work

```python
duration = bc.mine(4)   # Find a hash with 4 leading zeros
print("Mining duration:", duration)
bc.first.data.printBlock()
```

Higher difficulty values require exponentially more hashing work, illustrating the cost behind proof-of-work consensus.

## How It Works

Each block stores:

- `index` — position in the chain
- `payload` — arbitrary data
- `timestamp` — creation time
- `previousHash` — hash of the prior block (genesis uses 64 zeros)
- `ownHash` — SHA-256 of all fields above plus the nonce
- `nonce` — counter incremented during mining

Validation walks the chain and recomputes every hash; if any block's stored hash or `previousHash` link doesn't match, the chain is rejected.
