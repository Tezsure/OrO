import smartpy as sp

class StockClient(sp.Contract):
    def __init__(self):
        self.init(price =sp.int(0),marketCap=sp.int(0))
        
    @sp.entry_point
    def requestDataFromOrO(self,params):
        contract = sp.contract(sp.TRecord(ticker = sp.TString),params.oracleAddress,entry_point = "getDataFromOrO").open_some()
        
        requestRecord = sp.record(ticker = params.ticker)
        sp.transfer(requestRecord,sp.mutez(5000),contract)
        
    @sp.entry_point
    def receiveDataFromOrO(self,params):
        self.data.price = params.price
        self.data.marketCap = params.marketCap
        
@add_test(name="StockClientTest")
def test():
    scenario = sp.test_scenario()
    clientContract = StockClient()
    scenario += clientContract
    scenario += clientContract.requestDataFromOrO(ticker = "TSLA", oracleAddress=sp.address("KT1987")).run(sender=sp.address("KT1-AAA"), amount = sp.mutez(6000))
    scenario += clientContract.receiveDataFromOrO(price = 7096 , marketCap =7096000)
