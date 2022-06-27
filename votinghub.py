import smartpy as sp
fa12 = sp.io.import_script_from_url("https://smartpy.io/templates/FA1.2.py")

class Token(fa12.FA12):
    pass
        
class VotingHub(sp.Contract):
    def __init__(self, params):
        self.init(
            question = params.question,
            tokenPrice = params.tokenPrice,
            tokenContractAddress = params.contractAddress,
            votesRecord = sp.big_map()
        )

    @sp.entry_point
    def buyToken(self):
        sp.verify(sp.amount == self.data.tokenPrice)

        data_type = sp.TRecord(
            address = sp.TAddress, 
            value = sp.TNat
        ).layout(("address", "value"))

        contract = sp.contract(data_type, self.data.tokenContractAddress, "mint").open_some()

        data_to_be_sent = sp.record(
            address = sp.sender, 
            value = 1
        )
        sp.transfer(data_to_be_sent, sp.mutez(0), contract)

    @sp.entry_point
    def vote(self, params):
        
        data_type = sp.TRecord(
            address = sp.TAddress, 
            value = sp.TNat
        ).layout(("address", "value"))
        
        contract = sp.contract(data_type, self.data.tokenContractAddress, "burn").open_some()
        
        data_to_be_sent = sp.record(
            address = sp.sender, 
            value = 1
        )

        sp.transfer(data_to_be_sent, sp.mutez(0), contract)

        sp.if self.data.votesRecord.contains(params.option):
            self.data.votesRecord[params.option] +=1
        sp.else:
            self.data.votesRecord[params.option] = 1


@sp.add_test(name = "VotingHub")
def test():
    # create test users
    admin = sp.test_account("admin")
    alice = sp.test_account("alice")
    bob = sp.test_account("bob")

    # create scenario
    scenario = sp.test_scenario()

    # Add heading
    scenario.h1("Voting Hub")

    # Add subheading
    scenario.h2("Initialise the contract")

    token_metadata =  {
        "decimals": "0",
        "name": "Voting Token",
        "symbol": "vtoken"
    }

    token = Token(
        admin.address,
        config = fa12.FA12_config(),
        token_metadata=token_metadata,
    )

    # Add token to scenario
    scenario += token

    votingHub = VotingHub(
        sp.record(
            question = "What's your favouraite fruit?",
            tokenPrice = sp.mutez(100),
            contractAddress = token.address
        )
    )

    # Add votingHub to scenario
    scenario += votingHub

    token.setAdministrator(votingHub.address).run(sender=admin)

    votingHub.buyToken().run(sender=alice, amount=sp.mutez(100))

    votingHub.vote(
        option = "Banana"
    ).run(sender=alice, valid=True)

    votingHub.buyToken().run(sender=alice, amount=sp.mutez(100))

    votingHub.vote(
        option = "Apple"
    ).run(sender=alice, valid=True)

    scenario.show(votingHub.data)

    votingHub.buyToken().run(sender=bob, amount=sp.mutez(100))

    votingHub.vote(
        option = "Mango"
    ).run(sender=bob, valid=True)

    votingHub.buyToken().run(sender=bob, amount=sp.mutez(100))

    votingHub.vote(
        option = "Apple"
    ).run(sender=bob, valid=True)

    votingHub.vote(
        option = "Apple"
    ).run(sender=bob, valid=False)

    votingHub.vote(
        option = "Mango"
    ).run(sender=alice, valid=False)


