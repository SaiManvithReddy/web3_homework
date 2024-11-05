from web3 import Web3
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Connect to local provider
w3 = Web3(Web3.HTTPProvider(os.getenv("LOCAL_PROVIDER")))

# Set up the account
account = os.getenv("ANVIL_ACCOUNT")

# Address of the deployed contract (replace with the actual address after deploying)
contract_address = "0x663F3ad617193148711d28f5334eE4Ed07016602"  # Update this after deploying

# Load contract ABI
with open("compiled_contract.json") as json_file:
    compiled_contract = json.load(json_file)

contract_id = list(compiled_contract['contracts']['Contract.sol'].keys())[0]
contract_abi = compiled_contract['contracts']['Contract.sol'][contract_id]['abi']

# Create contract instance
new_contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# Update ID
update_tx = new_contract.functions.updateID(5341).build_transaction({
    'from': account,
    'nonce': w3.eth.get_transaction_count(account),
    'chainId': 31337,
})

# Sign and send the transaction
signed_update_tx = w3.eth.account.sign_transaction(update_tx, private_key=os.getenv("ANVIL_PRIVATE_KEY"))
update_tx_hash = w3.eth.send_raw_transaction(signed_update_tx.raw_transaction)
w3.eth.wait_for_transaction_receipt(update_tx_hash)

# Call viewMyId to get the updated StudentId
student_id = new_contract.functions.viewMyId().call()
print(f"Updated value is: {student_id}")
