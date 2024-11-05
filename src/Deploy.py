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
private_key = os.getenv("ANVIL_PRIVATE_KEY")

# Load compiled contract
with open("compiled_contract.json") as json_file:
    compiled_contract = json.load(json_file)

# Get contract details
contract_id = list(compiled_contract['contracts']['Contract.sol'].keys())[0]
contract_bytecode = compiled_contract['contracts']['Contract.sol'][contract_id]['evm']['bytecode']['object']
contract_abi = compiled_contract['contracts']['Contract.sol'][contract_id]['abi']

# Create contract instance
new_contract = w3.eth.contract(abi=contract_abi, bytecode=contract_bytecode)

# Build transaction for contract deployment
transaction = new_contract.constructor().build_transaction({
    'from': account,
    'nonce': w3.eth.get_transaction_count(account),
    'chainId': 31337,
})

# Sign and send the transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)


# Wait for transaction receipt
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

# Print the contract address
print(f"Contract deployed at: {tx_receipt.contractAddress}")
