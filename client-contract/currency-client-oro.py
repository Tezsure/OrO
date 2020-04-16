import smartpy as sp

class OracleClient(sp.Contract):
    def __init__(self):
        self.init(comments =sp.string(""),value = sp.int(0))
       
    @sp.entry_point
    def requestDataFromOracle(self,params):
        contract = sp.contract(sp.TRecord(convkey = sp.TString), params.address,entry_point="getDataFromOrO").open_some()
        requestData = sp.record(convkey = params.convkey)
        sp.transfer(requestData, sp.mutez(2000), contract)
   
    @sp.entry_point    
    def receiveDataFromOrO(self,params):
        self.data.comments = params.comments
        self.data.value = params.value


@sp.add_test(name="testOrOclient")
def test():
    client = OracleClient()
    scenario = sp.test_scenario()
    scenario += client
    scenario += client.requestDataFromOracle(address = sp.address('KT1897'), convkey = 'USD_INR').run(amount = sp.mutez(3000))
    scenario += client.receiveDataFromOrO(sp.record(comments = "Success", value = 76534))
