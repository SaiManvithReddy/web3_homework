from solcx import compile_standard, install_solc
import json

# Install a specific version of solc
install_solc('0.8.13')

def compile_contract():
    with open("Contract.sol", "r") as file:
        contract_source_code = file.read()

    compiled_sol = compile_standard({
        "language": "Solidity",
        "sources": {
            "Contract.sol": {
                "content": contract_source_code
            }
        },
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["*"],
                }
            }
        }
    })

    # Save the compiled contract to a JSON file
    with open("compiled_contract.json", "w") as json_file:
        json.dump(compiled_sol, json_file)

    return compiled_sol

if __name__ == "__main__":
    compiled_sol = compile_contract()
    print("Contract compiled successfully!")
