import smartpy as sp

class CompanyStockPriceOracle(sp.Contract):
    def __init__(self, admin):
        self.init(stockData = sp.map(tkey = sp.TString, tvalue = sp.TRecord(price=sp.TInt,marketCap=sp.TInt)), keysset = sp.set([admin]) , owner = admin)
    
    @sp.entry_point
    def feedData(self,params):
        sp.if (self.data.keysset.contains(sp.sender)):
            self.data.stockData[params.ticker] = sp.record(price = params.price, marketCap = params.marketCap)
            
    @sp.entry_point
    def addDataContributor(self,params):
        sp.if sp.sender == self.data.owner:
            self.data.keysset.add(params.contributor)
            
    @sp.entry_point
    def getDataFromOrO(self,params):
        errcd = sp.record(price = 0,marketCap=0)
        contract = sp.contract(sp.TRecord(price = sp.TInt, marketCap = sp.TInt),sp.sender,entry_point = "receiveDataFromOrO").open_some()
        
        sp.if sp.amount == sp.mutez(5000):
            sp.transfer(self.data.stockData[params.ticker],sp.mutez(0),contract)
        sp.else:
            sp.transfer(errcd,sp.amount,contract)

@sp.add_test(name="CompanyStockPriceOracleTest")
def test():
    scenario = sp.test_scenario()
    oracle = CompanyStockPriceOracle(sp.address('tz1XrHHchSehNudgAq1aQaoB4Bw7N4hZ1nkH'))
    scenario += oracle
    scenario += oracle.feedData(ticker = "TSLA", price = 7098 , marketCap = 7097000).run(sender=sp.address('tz1XrHHchSehNudgAq1aQaoB4Bw7N4hZ1nkH'))
    scenario += oracle.feedData(ticker = "FB", price = 5450 , marketCap = 54579100).run(sender=sp.address('tz1-AAA'))
    scenario += oracle.addDataContributor(contributor=sp.address("tz1-AAA")).run(sender=sp.address('tz1XrHHchSehNudgAq1aQaoB4Bw7N4hZ1nkH'))
    scenario += oracle.feedData(ticker = "FB", price = 5450 , marketCap = 54579100).run(sender=sp.address('tz1-AAA'))
    scenario += oracle.getDataFromOrO(ticker = "FB").run(sender=sp.address("KT1-AAA") , amount = sp.mutez(5000))
    scenario += oracle.getDataFromOrO(ticker = "FB").run(sender=sp.address("KT1-BBB") , amount = sp.mutez(4000))
