import smartpy as sp

class BitcoinToCurrencyDataOracle(sp.Contract):
    def __init__(self, admin):
        self.init(conversionData = sp.map(tkey = sp.TString, tvalue = sp.TRecord(buy=sp.TInt,sell=sp.TInt)), keysset = sp.set([admin]) , owner = admin)
    
    @sp.entry_point
    def feedData(self,params):
        sp.if (self.data.keysset.contains(sp.sender)):
            self.data.conversionData[params.currency] = sp.record(buy = params.buy, sell = params.sell)
            
    @sp.entry_point
    def addDataContributor(self,params):
        sp.if sp.sender == self.data.owner:
            self.data.keysset.add(params.contributor)
            
    @sp.entry_point
    def getDataFromOrO(self,params):
        errcd = sp.record(buy = 0,sell=0)
        contract = sp.contract(sp.TRecord(buy = sp.TInt, sell = sp.TInt),sp.sender,entry_point = "receiveDataFromOrO").open_some()
        
        sp.if sp.amount == sp.mutez(5000):
            sp.transfer(self.data.conversionData[params.currency],sp.mutez(0),contract)
        sp.else:
            sp.transfer(errcd,sp.amount,contract)

@sp.add_test(name="BTCUSDTest")
def test():
    scenario = sp.test_scenario()
    oracle = BitcoinToCurrencyDataOracle(sp.address('tz1beX9ZDev6SVVW9yJwNYA89362ZpWuDwou'))
    scenario += oracle
    scenario += oracle.feedData(currency = "USD", buy = 7098 , sell = 7097).run(sender=sp.address('tz1beX9ZDev6SVVW9yJwNYA89362ZpWuDwou'))
    scenario += oracle.feedData(currency = "INR", buy = 545791 , sell = 545791).run(sender=sp.address('tz1-AAA'))
    scenario += oracle.addDataContributor(contributor=sp.address("tz1-AAA")).run(sender=sp.address('tz1beX9ZDev6SVVW9yJwNYA89362ZpWuDwou'))
    scenario += oracle.feedData(currency = "INR", buy = 545791 , sell = 545791).run(sender=sp.address('tz1-AAA'))
    scenario += oracle.getDataFromOrO(currency = "INR").run(sender=sp.address("KT1-AAA") , amount = sp.mutez(5000))
    scenario += oracle.getDataFromOrO(currency = "INR").run(sender=sp.address("KT1-BBB") , amount = sp.mutez(4000))
    
    
