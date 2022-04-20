from cgi import print_arguments
from scripts.helpful_scripts import get_account
from brownie import network, config, interface
from scripts.get_weth import get_weth
from web3 import Web3

# Amount is 0.1
amount = Web3.toWei(0.1, "ether")


def main():
    account = get_account()
    erc20_address = config["networks"][network.show_active()]["weth_token"]

    # call get weth contract get_weth()
    if network.show_active() in ["mainnet-fork"]:
        get_weth()
    # ABI
    # Address
    lending_pool = get_lending_pool()

    # Approve sending out ERC20 tokens
    approve_erc20(amount, lending_pool.address, erc20_address, account)

    # Deposit
    print("Root: ... Depositing ...")
    tx = lending_pool.deposit(
        erc20_address, amount, account.address, 0, {"from": account}
    )
    tx.wait(1)
    print("Root: Success! Deposit Complete")

    # how much funds can we borrow ?
    borrowable_eth, total_debt = get_borrowable_data(
        lending_pool,
        account,
    )

    # Borrow some DAI
    print("Root: Borrow Some DAI")
    dai_eth_price = get_asset_price(
        config["networks"][network.show_active()]["dai_eth_price_feed"]
    )
    amount_dai_to_borrow = (1 / dai_eth_price) * (borrowable_eth * 0.95)
    # borrowable_eth -> borrowable_dai * 95% (we are borrowing 95% of our collateral to avoid liquidation)
    print(f"Root: We are going to borrow {amount_dai_to_borrow} DAI")

    dai_address = config["networks"][network.show_active()]["dai_token"]
    borrow_tx = lending_pool.borrow(
        dai_address,
        Web3.toWei(amount_dai_to_borrow, "ether"),
        1,
        0,
        account.address,
        {"from": account},
    )
    borrow_tx.wait(1)
    print("Root: DAI successfully borrowed")
    # Show Account Information
    get_borrowable_data(lending_pool, account)

    # Repay borrowed assets
    #repay_all(amount, lending_pool, account)
    print(
        "Root: Your last Deposit will be used to repay your borrowed Assets with Aave, Brownie and Chainlink!"
    )


def repay_all(amount, lending_pool, account):
    approve_erc20(
        Web3.toWei(amount, "ether"),
        lending_pool,
        config["networks"][network.show_active()]["dai_token"],
        account,
    )
    repay_tx = lending_pool.repay(
        config["networks"][network.show_active()]["dai_token"],
        amount,
        1,
        account.address,
        {"from": account},
    )
    repay_tx.wait(1)
    print("Root: Borrowed Asset Repaid! ")


def get_asset_price(price_feed_address):
    # ABI
    # Address
    dai_eth_price_feed = interface.AggregatorV3Interface(price_feed_address)

    # Get the Latest Price
    latest_price = dai_eth_price_feed.latestRoundData()[1]
    converted_latest_price = Web3.fromWei(latest_price, "ether")
    print(f"Root: The DAI/ETH price is - {Web3.fromWei(latest_price, 'ether')}")
    return float(converted_latest_price)


def get_borrowable_data(lending_pool, account):
    (
        total_collateral_eth,
        total_debt_eth,
        available_borrow_eth,
        current_liquidation_threshold,
        ltv,
        health_factor,
    ) = lending_pool.getUserAccountData(account.address)
    # Data comes in Wei - Convert it from Wei
    available_borrow_eth = Web3.fromWei(available_borrow_eth, "ether")
    total_collateral_eth = Web3.fromWei(total_collateral_eth, "ether")
    total_debt_eth = Web3.fromWei(total_debt_eth, "ether")
    print(f"Root: You have - {total_collateral_eth} worth of ETH deposited")
    print(f"Root: You have - {total_debt_eth} worth of ETH borrowed")
    print(f"Root: You can borrow - {available_borrow_eth} worth of ETH")
    # Return Data in float
    return (float(available_borrow_eth), float(total_debt_eth))


# for other contracts to use your tokens you have to approve them
def approve_erc20(amount, spender, erc20_address, account):
    # ABI
    # Address
    print("Root: ... Approving ERC20 Token...")
    erc20 = interface.IERC20(erc20_address)
    tx = erc20.approve(spender, amount, {"from": account})
    tx.wait(1)
    print("Root: Transaction Approved! ")
    return tx


def get_lending_pool():
    lending_pool_addresses_provider = interface.ILendingPoolAddressesProvider(
        config["networks"][network.show_active()]["lending_pool_addresses_provider"]
    )
    lending_pool_address = lending_pool_addresses_provider.getLendingPool()
    # ABI
    # Address
    lending_pool = interface.ILendingPool(lending_pool_address)
    return lending_pool
