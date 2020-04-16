import smartpy as sp

class OracleClient(sp.Contract):
    def __init__(self):
        self.init(temperature = sp.int(0), humidity = sp.int(0),pressure = sp.int(0))
       
    @sp.entry_point
    def requestDataFromOracle(self,params):
        contract = sp.contract(sp.TRecord(city = sp.TString), params.address,entry_point="getDataFromOrO").open_some()
        requestData = sp.record(city = params.city)
        sp.transfer(requestData, sp.mutez(3000), contract)
   
    @sp.entry_point    
    def receiveDataFromOrO(self,params):
        self.data.temperature = params.temperature
        self.data.pressure = params.pressure
        self.data.humidity = params.humidity


@sp.add_test(name="testOrOclient")
def test():
    client = OracleClient()
    scenario = sp.test_scenario()
    scenario += client
    scenario += client.requestDataFromOracle(address = sp.address('KT1897'), city = 'Bangalore').run(amount = sp.mutez(3000))
    scenario += client.receiveDataFromOrO(sp.record(humidity = 10, pressure = 20, temperature = 57))
