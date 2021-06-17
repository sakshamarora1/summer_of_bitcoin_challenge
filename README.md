# Summer of Bitcoin Code Challenge

`mempool.csv` contains all the transactions in the format:

1. txid - Transaction ID
2. fee - Transaction Fee
3. weight - Transaction Weight
4. parent_txid - List of Transaction IDs of the transactions's (Unconfirmed) Parent Transaction IDs

The generated `block.txt` file contains the Transaction IDs of all the transactions (included in the miner's constructed block) seperated by newlines that will maximize the total fees the miner collects such that the total sum of weights do not exceed the maximum weight of 4,000,000 in the block.

#### **The main solution file is named [solution.py](solution.py).**

The previous solutions folder contains the solutions I started off with using which I got to my current main solution!

The `result.txt` file contains the - 

1. Number of transactions included in the generated block
2. Total Weight of Block
3. Total Fee of all transactions in the block

## Approach / Logic

```
1. Read mempool.csv and create MempoolTransaction object for each transaction.

2. Sort all the transactions in descending order, by prioritizing the transactions with higher fee/weight ratio.

3. Iterate through all the transactions in mempool and -

    a. Check if the weight of the can be accomodated in the block such that the total weight of all the transactions in the block doesn't exceed 4,000,000.

    b. Check if their are any parent transactions of the current transactions. If there are any and are not included in the block, we don't include the current transaction and we keep track of it and its parent transactions.

    c. If both of the conditions (weight of current transaction + total weight of previous transactions <= 4,000,000 and all parent transactions of the current transaction are included), we add the transaction to the block and append it to the `block.txt` file on a newline.

    d. We then check if the current transaction was a parent transaction of any previous (having high fee/weight ratio) non-included transaction and check if that previous child transaction is now eligible to be included in the block by checking if all the parents of that child transactions are included.
```