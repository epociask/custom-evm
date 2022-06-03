# custom-evm
Custom python EVM implementation that's (_hopefully_) compatible for running standard EVM bytecode.

## WHY?
The EVM is an incredibly niche technology within blockchain. While very misunderstod, its a vital component to blockchain as a whole and will likely live for a long time. Currently, any documentation surrounding the inner-workings of the EVM at a bytecode level is either lackluster or flat out wrong.

**TLDR:** This project is done to disambiguate the underlying functionality of the EVM and hopefully provide a learning experience for other blockchain enthusiasts to use. 

## Operations Supported
- [ ] `DELEGATE_CALL` functionality
- [ ] Gas computations and exceeded gas haulting
- [ ] Standard precompiles
- [ ] Storage representation
- [ ] Stack representation
- [ ] Memory representation
- [ ] Execution state opcodes (`DIFFICULTY`, `BLOCKHASH`)
- [ ] Arithmetic operations
- [ ] Jumping and branching
- [ ] Jump analysis logic
- [ ] All `DUP` and `PUSH` opcodes

## Testing 
There a two types of tests for this project:

1. Integration
These are TBD but will use compiled solidity bytecode for different ERC-20 contracts to test standard functionality (_transfers_, _approvals_, __) 

**NOTE** 
These will be the most time consuming to debug, correct, and properly test.


2. Unit
These are located within `/tests` and test:
* opcode snippets against intepreter
* Functionality of standard machine constructs (`stack`, `memory`, `storage`)