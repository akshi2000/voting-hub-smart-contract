# Voting Hub Smart Contract

A smart contract on tezos blockchain that handles a question and some answers. Users are able to vote for their answer. Before voting, the user needs to buy a token to vote (vtoken). vtoken is a fungible token made using FA1.2 standard. Multiple vtokens can be bought and used to vote multiple times. There is no vtoken total supply limit, but fixed price to mint that is 100 microtezos. One vtoken can only be used for voting once.

## VotingHub Entrypoints

- buyToken: Requires 100 micro tezos as transaction amount. A vtoken will be minted for the sender.

- vote: Requires no amount. A vtoken will be burned for the sender. Transaction will be cancelled if there's no vtoken for the seder. It requires following parameters:


| Parameter | Type      | Description                                                   |
| :-------- | :-------- | :------------------------------------------------------------ |
| `option`    | `string` | **Required**. Option that user want to vote for |


## Contract Addresses (Deployed on ithacanet):

- Voting Hub: [KT1SjtswtaQemT6DctE6wxxgKW5dzUFH7BWP](https://better-call.dev/ithacanet/KT1SjtswtaQemT6DctE6wxxgKW5dzUFH7BWP/)
- Token: [KT1VDnFtVE6KceeQCVSFduBtFqRvy4Kp5CRe](https://better-call.dev/ithacanet/KT1VDnFtVE6KceeQCVSFduBtFqRvy4Kp5CRe/)

Note: Token contract address can only be used to view number of supplied tokens, operations can only be performed by Voting Hub

## TODO

* [ ] Build a frontend to buy vtokens, vote for options and view voted option
