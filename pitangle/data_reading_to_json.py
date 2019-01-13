from datetime import datetime
from iota import Address, Iota, Transaction, TryteString
import json

in_file = open("tangle/address_dump.conf", "rb") # opening for [r]eading as [b]inary
ADDRESS = in_file.read() # if you only wanted to read 512 bytes, do .read(512)
in_file.close()

# 0. Where is data stored?
receiver = Address(
    ADDRESS
)

# 1. Connect to public node
api = Iota("https://durian.iotasalad.org:14265")

# 2. Retrieve all transactions
txs = api.find_transactions(addresses=[receiver])
data = []

# 3. Iterate over transactions, decode and print
for tx_hash in txs["hashes"]:
    tx_hash_b = bytes(tx_hash)
    tx_data_trytes = api.get_trytes([tx_hash_b])
    tryte_str = str(tx_data_trytes["trytes"][0])

    tx = Transaction.from_tryte_string(tryte_str)

    timestamp = datetime.fromtimestamp(tx.timestamp)
    tx_data = json.loads(str(tx.signature_message_fragment.decode()))
    print(tx_data)
    data.append(tx_data)

with open('data.json', 'w') as outfile:
    json.dump(data, outfile)
