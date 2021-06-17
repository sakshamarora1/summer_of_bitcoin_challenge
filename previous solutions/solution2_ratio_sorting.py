class MempoolTransaction:
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
        return f"txid: {self._txid}\nfee: {self._fee}\nweight: {self._weight}\nparents: {self._parents}\n"


class Block:
    def __init__(self):
        self.maxWeight = 4_000_000
        self.blockWeight = 0
        self.blockFee = 0
        self.transactions = set()

    def addTransaction(self, transaction: MempoolTransaction):
        self.transactions.add(transaction.get_txid())
        self.updateBlock(transaction)

    def validateTransaction(self, transaction: MempoolTransaction):
        if self.blockWeight + transaction.get_weight() > self.maxWeight:
            return False
        for parent in transaction.get_parents():
            if parent not in self.transactions:
                return False
        return True

    def updateBlock(self, transaction: MempoolTransaction):
        self.blockFee += transaction.get_fee()
        self.blockWeight += transaction.get_weight()

    def write(self, fname):
        with open(fname, "w") as f:
            f.write("\n".join(self.transactions))

    def __len__(self):
        return len(self.transactions)


def sort_transactions(transactions):
    return sorted(
        transactions, key=lambda tx: tx.get_fee()/tx.get_weight(), reverse=True
    )


def parse_mempool_csv():
    """Parse the CSV file and return a list of MempoolTransactions."""
    with open("mempool.csv") as f:
        f.readline()
        return [MempoolTransaction(*line.strip().split(",")) for line in f.readlines()]


if __name__ == "__main__":
    transactions = parse_mempool_csv()
    sortedtransactions = sort_transactions(transactions)

    block = Block()
    i = 0
    while i < len(sortedtransactions):
        tx = sortedtransactions[i]
        if block.validateTransaction(tx):
            block.addTransaction(tx)
        i += 1

    block.write("block_ratio_sorting.txt")
    print(block.blockWeight)
    print(block.blockFee)
    print(len(block))
