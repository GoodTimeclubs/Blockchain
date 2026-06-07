# Blockchain

A minimal Python blockchain implementation that demonstrates block hashing, chain validation, proof-of-work mining, author authentication via X.509 certificates, and longest-chain consensus.

## Overview

This project is an educational, from-scratch implementation of the core mechanics behind a blockchain. Blocks are stored as nodes in a linked list, each linked to its predecessor by a SHA-256 hash. Every block is digitally signed by its author, and the author's identity is validated against a trusted Certificate Authority (CA). The chain can be validated, tampered with, mined against a configurable difficulty target, and reconciled with competing chains using a longest-chain rule.

## Features

- **SHA-256 block hashing** over payload, timestamp, previous hash, index, and nonce
- **Linked-list chain structure** via custom `Node` and `Block` classes
- **Proof-of-work mining** with adjustable difficulty (leading-zero hash target)
- **Author authentication** — each block is signed with an RSA private key, and the signer's X.509 certificate is verified against a trusted CA
- **Chain validation** that detects tampering of hashes, broken links, and untrusted signers
- **Sabotage method** to demonstrate how altering a block invalidates the chain
- **Longest-chain resolution** (`resolve`) to pick the longest valid chain among competing candidates

## Project Structure

```
Blockchain/
├── Block.py          # Block data structure (payload, hashes, nonce, signature, ...)
├── Node.py           # Linked-list node wrapping a Block
├── Blockchain.py     # Chain logic: add, validate, sabotage, mine, resolve
├── Authorization.py  # Signing and X.509 certificate validation against a CA
├── Main.py           # Example usage and longest-chain demo
└── certs/            # Keys and certificates (git-ignored, see below)
```

## Requirements

- Python 3.x
- [`cryptography`](https://pypi.org/project/cryptography/) — for signing and X.509 certificate handling

```bash
pip install cryptography
```

## Certificates

Signing and verification require a `certs/` directory (git-ignored) containing the
author's private key, the author's certificate, and the trusted CA certificate.
The default CA filename is `cacert.pem` (configurable in `Authorization`).

You can generate a self-signed CA and an author certificate signed by it with OpenSSL:

```bash
# 1) Create the CA key and a self-signed CA certificate
openssl req -x509 -newkey rsa:2048 -nodes -keyout ca.key.pem -out certs/cacert.pem -days 365 -subj "/CN=Test CA"

# 2) Create the author's key and a certificate signing request (CSR)
openssl req -newkey rsa:2048 -nodes -keyout certs/alice.key.pem -out alice.csr.pem -subj "/CN=Alice"

# 3) Sign the author's CSR with the CA to produce the author certificate
openssl x509 -req -in alice.csr.pem -CA certs/cacert.pem -CAkey ca.key.pem -CAcreateserial -out certs/alice.cert.pem -days 365
```

If the private key is password-protected, you will be prompted for the passphrase when signing.

## Usage

Run the example:

```bash
python Main.py
```

### Building a chain

Each block carries the author's name and the filenames of the certificate and
private key (relative to `certs/`). The block is mined and signed automatically.

```python
from Blockchain import Blockchain

bc = Blockchain()
bc.addBlock("hallo", "Alice", "alice.cert.pem", "alice.key.pem")
bc.addBlock("das",   "Alice", "alice.cert.pem", "alice.key.pem")
bc.addBlock("ist",   "Alice", "alice.cert.pem", "alice.key.pem")

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
# Mine the block at the given index until its hash has `difficulty` leading zeros
duration = bc.mine(4, 0)   # difficulty 4, block index 0
print("Mining duration:", duration)
bc.first.data.printBlock()
```

Higher difficulty values require exponentially more hashing work, illustrating the cost behind proof-of-work consensus.

### Resolving competing chains (longest-chain rule)

```python
longest = bc.resolve(chain_a, chain_b)   # returns the longest valid chain
longest.printBlockchain()
```

`resolve` returns the longer of the two candidate chains if it is valid and shares
the same genesis payload. On equal length it returns the first valid chain, or
`None` if neither chain is valid.

## How It Works

Each block stores:

- `index` — position in the chain
- `payload` — arbitrary data
- `timestamp` — creation time
- `previousHash` — hash of the prior block (genesis uses 64 zeros)
- `ownHash` — SHA-256 of all fields above plus the nonce
- `nonce` — counter incremented during mining
- `signer` — human-readable name of the author
- `signature` — RSA signature of the payload
- `publicKeyFilename` / `prvKeyFilename` — certificate and key used to sign/verify

Validation walks the chain and, for every block, recomputes the hash, checks that
`previousHash` links to the prior block, and verifies that the signer's certificate
was issued by the trusted CA. If any check fails, the chain is rejected.
