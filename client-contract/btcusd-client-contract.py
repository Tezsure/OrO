import smartpy as sp

class BTCUSDClient(sp.Contract):
    def __init__(self):
        self.init(buy =sp.int(0),sell=sp.int(0))
        
    @sp.entry_point
    def requestDataFromOrO(self,params):
        contract = sp.contract(sp.TRecord(currency = sp.TString),params.oracleAddress,entry_point = "getDataFromOrO").open_some()
        
        requestRecord = sp.record(currency = params.currency)
        sp.transfer(requestRecord,sp.mutez(5000),contract)
        
    @sp.entry_point
    def receiveDataFromOrO(self,params):
        self.data.buy = params.buy
        self.data.sell = params.sell
        
@add_test(name="BTCUSDClienttest")
def test():
    scenario = sp.test_scenario()
    clientContract = BTCUSDClient()
    scenario += clientContract
    scenario += clientContract.requestDataFromOrO(currency = "USD",oracleAddress = sp.address("KT1987")).run(sender=sp.address("KT1-AAA"), amount = sp.mutez(6000))
    scenario += clientContract.receiveDataFromOrO(buy = 7096 , sell =7096)
        
