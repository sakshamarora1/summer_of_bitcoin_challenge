import os


class MempoolTransaction:
    """Base Transaction Class"""

    def __init__(self, txid, fee, weight, parents):
        self._txid = txid
        self._fee = int(fee)
        self._weight = int(weight)
        self._parents = parents.split(";") if parents != "" else []

    def get_txid(self):
        return self._txid

    def get_fee(self):
        return self._fee

    def get_weight(self):
        return self._weight

    def get_parents(self):
        return self._parents

    def __repr__(self):
        return f"txid: {self._txid}\nfee: {self._fee}\nweight: {self._weight}\nparents: {self._parents}"


class Block:
    """Block class to keep track of all the variables related to the block"""

    def __init__(self, filename="block.txt"):
        self.maxWeight = 4_000_000
        self.blockWeight = 0
        self.blockFee = 0
        self.transactions = set()

        self.filename = os.path.join(os.getcwd(), filename)
        if os.path.exists(self.filename):
            os.remove(self.filename)

        # This parent_child_mapping dictionary is used to keep track of those parent transactions and their children transactions
        # that weren't included and might have a chance to be included if the parent transaction is included later on.
        self.parent_child_mapping = {}

        # This child_wait dictionary is used to keep track of all those transactions that weren't included in the block due to their
        # parents not being in the block currently, it stores the number of parents of a transaction not in the block at a given moment
        # as soon as all its parents are included (number hits 0), we try to include the transaction if possible and recursively
        # check for their parents if any
        self.child_wait = {}

    def addTransaction(self, transaction: MempoolTransaction):
        self.transactions.add(transaction.get_txid())
        self.updateBlock(transaction)
        with open(self.filename, "a") as f:
            f.write(transaction.get_txid() + "\n")

        # Check if the transaction was a parent of any previous transaction that wasn't included in the block
        children = block.parent_child_mapping.pop(transaction.get_txid(), [])
        
        for child_id, child in children:
            
            # Update the number of parent transactions a child transaction has left for it to be considered again
            if child_id in self.child_wait:
                self.child_wait[child_id] -= 1
                
                if self.child_wait[child_id] == 0:
                    # If all the parent transactions are in the block, then we remove it from the mapping and check if it can be
                    # included in the block
                    self.child_wait.pop(child_id)
                
                    if self.validateTransaction(child):
                        self.addTransaction(child)

    def validateTransaction(self, transaction: MempoolTransaction):
        # Check if the transaction can be included without exceeding the maximum weight limit of the block
        if self.blockWeight + transaction.get_weight() > self.maxWeight:
            return False

        include = True
        tx_id = transaction.get_txid()
        for parent in transaction.get_parents():
            if parent not in self.transactions:
                # If the parent transaction is not in the block then we keep track of it using the parent_child_mapping
                if parent not in self.parent_child_mapping:
                    self.parent_child_mapping[parent] = []
                self.parent_child_mapping[parent].append((tx_id, transaction))

                if tx_id not in self.child_wait:
                    self.child_wait[tx_id] = 0
                # We increment the number of parents of the current transaction that are not included in the block as we
                # iterate through the entire loop
                self.child_wait[tx_id] += 1
                # If any of the parent transaction is not included in the block, then the current transaction is not eligible
                # to be included
                include = False
        return include

    def updateBlock(self, transaction: MempoolTransaction):
        # Update the total block weight and fees collection after every included transaction
        self.blockFee += transaction.get_fee()
        self.blockWeight += transaction.get_weight()

    def __len__(self):
        return len(self.transactions)


def sort_transactions(txs):
    """
    Returns a list of MempoolTransactions that are sorted in descending order
    by taking the ratio of the fee and the weight of a transaction.
    """
    return sorted(txs, key=lambda tx: tx.get_fee() / tx.get_weight(), reverse=True)


def parse_mempool_csv():
    """Parse the CSV file and return a list of MempoolTransactions."""
    with open("mempool.csv") as f:
        f.readline()
        return [MempoolTransaction(*line.strip().split(",")) for line in f.readlines()]


if __name__ == "__main__":
    transactions = parse_mempool_csv()
    sortedtransactions = sort_transactions(transactions)

    block = Block()
    for tx in sortedtransactions:
        # Iterate through all the transactions in the sorted list and if the transaction is valid then we add it to the block.
        if block.validateTransaction(tx):
            block.addTransaction(tx)

    message = f"Total Number of transactions in the block: {len(block)}\nTotal Weight of Block: {block.blockWeight}\nTotal Fee of all transactions in the block: {block.blockFee}"
    with open("result.txt", "w") as f:
        f.write(message)
    print(message)
