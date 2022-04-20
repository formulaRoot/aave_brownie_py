
Objectives: 

1. Swap ETH to WETH (Wrapped Ether) to enable ETH to work with other ERC20 Tokens 
2. Deposit the swapped WETH into Aave[https://docs.aave.com/developers/core-contracts/pool] using the deposit()
3. Borrow assest with the ETH as Collateral 
 - Approve sending out ERC20 tokens. Other contracts need to be approve before they can use your tokens
 - Chech how much you can borrow 
 - Borrow  
4. Pay everything back
- Repay the borrowed tokens  

----------

Additional Tasks:
1. Interact with decentralized exchanges (DEX)
- Paraswap 
- Uniswap

-----------

Testing:
1. Integration Test: Kovan 
2. Unit test: Mainnet-fork 