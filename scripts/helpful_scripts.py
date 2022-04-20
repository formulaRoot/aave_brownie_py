from brownie import (
    accounts,
    network,
    config,
)


FORKED_LOCAL_ENVIROMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIROMENTS = [
    "development",
    "ganache-local",
    "gabache",
    "mainnet-fork",
    "hardhat",
]


def get_account(index=None, id=None):

    if index:
        return accounts[index]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIROMENTS:
        print(accounts[0].balance())
        return accounts[0]
    if id:
        return accounts.load(id)
    if network.show_active() in config["networks"]:
        return accounts.add(config["wallets"]["from_key"])
    return None
