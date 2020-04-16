import smartpy as sp

class WeatherOracle(sp.Contract):
    def __init__(self, admin):
        self.init(apidata = sp.map(tkey = sp.TString, tvalue = sp.TRecord(humidity=sp.TInt, temperature = sp.TInt, pressure = sp.TInt)), keysset = sp.set([admin]))
    
    
    @sp.entry_point
    def feedData(self,params):
        sp.if (self.data.keysset.contains(sp.sender)):
            self.data.apidata[params.city] = sp.record(humidity = params.humidity, temperature = params.temperature, pressure = params.pressure)
            
            
    @sp.entry_point
    def getDataFromOrO(self,params):
        errrcd = sp.record(humidity=0 , temperature=0 , pressure=0)
        contract = sp.contract(sp.TRecord(humidity = sp.TInt, temperature = sp.TInt, pressure = sp.TInt),sp.sender,entry_point = "receiveDataFromOrO").open_some()
        sp.if sp.amount == sp.mutez(3000):
            sp.if self.data.apidata.contains(params.city):
                sp.transfer(self.data.apidata[params.city], sp.mutez(0), contract)
            sp.else:
                sp.transfer(errrcd, sp.mutez(0), contract)
        sp.else:
            sp.transfer(errrcd, sp.mutez(0), contract)
                
            

@sp.add_test(name="testWeatherOrO")
def test():
    scenario = sp.test_scenario()
    oracle = WeatherOracle(sp.address('tz1beX9ZDev6SVVW9yJwNYA89362ZpWuDwou'))
    scenario += oracle
    scenario += oracle.feedData(humidity = 100, temperature = 38, pressure = 100, city = 'Bangalore')
    scenario += oracle.getDataFromOrO(city = 'Bangalore').run(sender = sp.address('KT1XXDS'), amount = sp.mutez(2999))