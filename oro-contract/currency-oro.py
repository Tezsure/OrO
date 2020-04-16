import smartpy as sp

class CurrencyConverter(sp.Contract):
    def __init__(self,admin):
        self.init(apidata = sp.map(tkey = sp.TString, tvalue = sp.TInt), keysset=sp.set([admin]))
        
    @sp.entry_point
    def getRequestFromClient(self,params):
        sp.if self.data.apidata.contains(params.convkey):
            sp.if sp.amount==sp.mutez(2000):
                value = self.data.apidata[params.convkey]
                comments = "Success"
                c = sp.contract(sp.TRecord(value = sp.TInt, comments = sp.TString),sp.sender,entry_point="receiveDataFromOrO").open_some()
                mydata = sp.record(value = value,comments = comments)
                sp.transfer(mydata,sp.mutez(0),c)
            sp.else:
                value = 0
                comments = "Invalid amount"
                c = sp.contract(sp.TRecord(value = sp.TInt, comments = sp.TString),sp.sender,entry_point="receiveDataFromOrO").open_some()
                mydata = sp.record(value = value,comments = comments)
                sp.transfer(mydata,sp.mutez(0),c)
        sp.else:
            value = 0
            comments = "Bad request"
            c = sp.contract(sp.TRecord(value = sp.TInt, comments = sp.TString),sp.sender,entry_point="receiveDataFromOrO").open_some()
            mydata = sp.record(value = value,comments = comments)
            sp.transfer(mydata,sp.mutez(0),c)
            
    @sp.entry_point
    def feedData(self,params):
        sp.if self.data.keysset.contains(sp.sender):
            self.data.apidata[params.key]=params.value
        
@sp.add_test(name="test")
def test():
    oracle = CurrencyConverter(sp.address("tz1XrHHchSehNudgAq1aQaoB4Bw7N4hZ1nkH"))
    scenario = sp.test_scenario()
    scenario += oracle
    scenario += oracle.feedData(key = "USD_INR",value=76534).run(sender=sp.address("tz1XrHHchSehNudgAq1aQaoB4Bw7N4hZ1nkH"))
    scenario += oracle.getRequestFromClient(convkey="USD_INR").run(sender=sp.address("KT1987"))
