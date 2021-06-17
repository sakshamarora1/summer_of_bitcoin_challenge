# Summer of Bitcoin Code Challenge

`mempool.csv` contains all the transactions in the format:

1. txid - Transaction ID
2. fee - Transaction Fee
3. weight - Transaction Weight
4. parent_txid - List of Transaction IDs of the transactions's (Unconfirmed) Parent Transaction IDs

### The generated `block.txt` file contains the Transaction IDs of all the transactions (included in the miner's constructed block) seperated by newlines that will maximize the total fees the miner collects such that the total sum of weights do not exceed the maximum weight of 4,000,000 in the block.

## **The main solution file is named [solution.py](solution.py).**

The previous solutions folder contains the solutions I started off with using which I got to my current main solution!

The `result.txt` file contains the - 

1. Number of transactions included in the generated block
2. Total Weight of Block
3. Total Fee of all transactions in the block
