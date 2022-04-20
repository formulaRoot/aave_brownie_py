from brownie import interface, config, network
from scripts.helpful_scripts import get_account


def main():
    get_weth()


# Convert ETH to WETH
def get_weth():
    """
    Mints WETH by depositing ETH
    """
    # Get the following:
    # ABI
    # Address

    account = get_account()
    weth = interface.IWeth(config["networks"][network.show_active()]["weth_token"])
    tx = weth.deposit({"from": account, "value": 0.1 * 10**18})
    tx.wait(1)
    print("Root: Success! You got: 0.1 WETH")
    return tx
