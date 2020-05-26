# An illustrative example of a "trusted" oracle contract.
# Author: Mike Radin, github.com/anonymoussprocket
# Licensed under the Apache License, Version 2.0.

import smartpy as sp

class ExchangeRateConsumer(sp.Contract):
    def __init__(self, oracle):
        self.init(
            oracle = oracle,
            currencyPair = sp.string(""),
            value = sp.nat(0),
            precision = sp.nat(0),
            timestamp = sp.timestamp(0),
            source = sp.string(""))

    @sp.entry_point
    def sendQuery(self, params):
        rtype = sp.TRecord(
                currencyPair = sp.TString,
                value = sp.TNat,
                precision = sp.TNat,
                timestamp = sp.TTimestamp,
                source = sp.TString)
        ptype = sp.TRecord(
            currencyPair = sp.TString,
            callback = sp.TContract(rtype)
        )

        getHandle = sp.contract(ptype, self.data.oracle, entry_point = "processDataRequest").open_some()

        args = sp.record(
            currencyPair = params.currencyPair,
            callback = sp.contract(rtype,
                            sp.to_address(sp.self),
                            entry_point = "receiveData").open_some()
            )
        sp.transfer(args, sp.tez(1000), getHandle)

    @sp.entry_point
    def receiveData(self, params):
        self.data.currencyPair = params.currencyPair
        self.data.value = params.value
        self.data.precision = params.precision
        self.data.timestamp = params.timestamp
        self.data.source = params.source

class ExchangeRateOracle(sp.Contract):
    def __init__(self, admin):
        self.init(
            feed = sp.map(
                tkey = sp.TString,
                tvalue =
                    sp.TRecord(
                        value = sp.TNat,
                        precision = sp.TNat,
                        timestamp = sp.TTimestamp,
                        source = sp.TString
                )),
            feedQueryCost = sp.map(tkey = sp.TString, tvalue = sp.TMutez),
            admin = admin,
            operators = sp.set(),
            registeredPairs = sp.set()
        )
        
    @sp.entry_point
    def processDataRequest(self, params):
        sp.verify(self.data.registeredPairs.contains(params.currencyPair), message = "Unregistered currency pair")
        sp.verify(sp.amount > self.data.feedQueryCost[params.currencyPair], message = "Incorrect query fee")
        sp.verify(self.data.feed.contains(params.currencyPair), message = "Data not available")

        record = self.data.feed[params.currencyPair]

        sp.transfer(
            sp.record(
                currencyPair = params.currencyPair,
                value = record.value,
                precision = record.precision,
                timestamp = record.timestamp,
                source = record.source
                ),
            sp.tez(0),
            params.callback)

    @sp.entry_point
    def updateFeed(self, params):
        sp.verify(self.data.operators.contains(sp.sender), message = "Privileged operation")
        self.data.feed[params.currencyPair] = sp.record(
            value = params.value,
            precision = params.precision,
            timestamp = params.timestamp,
            source = params.source)

    @sp.entry_point
    def registerFeed(self, params):
        sp.verify(sp.sender == self.data.admin, message = "Privileged operation")
        sp.verify(~ self.data.feed.contains(params.currencyPair), message = "Currency pair already registered")
        self.data.registeredPairs.add(params.currencyPair)
        self.data.feedQueryCost[params.currencyPair] = params.cost
    
    @sp.entry_point
    def updateOperatorList(self, params):
        sp.verify(sp.sender == self.data.admin, message = "Privileged operation")
        self.data.operators = params.operators
    
    @sp.entry_point
    def updateAdmin(self, params):
        sp.verify(sp.sender == self.data.admin, message = "Privileged operation")
        pass
        
    @sp.entry_point
    def setDelegate(self, params):
        sp.verify(sp.sender == self.data.admin, message = "Privileged operation")
        pass
        
    @sp.entry_point
    def transferBalance(self, params):
        sp.verify(sp.sender == self.data.admin, message = "Privileged operation")
        pass

@sp.add_test(name="ExchangeRateOracle Tests")
def test():
    scenario = sp.test_scenario()
    scenario.h1("ExchangeRateOracle Tests")

    admin = sp.test_account("Admin")
    scenario.show(admin)

    operatorA = sp.test_account("operatorA")
    scenario.show(operatorA)

    operatorB = sp.test_account("operatorB")
    scenario.show(operatorB)

    caller = sp.test_account("caller")
    scenario.show(caller)

    oracle = ExchangeRateOracle(admin.address)
    scenario.register(oracle)

    consumer = ExchangeRateConsumer(oracle.address)
    scenario.register(consumer)

    scenario += oracle.updateOperatorList(operators = sp.set([operatorA.address, operatorB.address])).run(sender = admin)
    scenario += oracle.registerFeed(currencyPair = "USDEUR", cost = sp.mutez(1000)).run(sender = admin)
    scenario += oracle.updateFeed(currencyPair = "USDEUR", value = sp.nat(92), precision = sp.nat(2), timestamp = sp.timestamp(0), source = "Trusted Source").run(sender = operatorA)

    scenario += consumer.sendQuery(currencyPair = "USDEUR").run(sender = caller, amount = sp.mutez(1000))
    scenario.verify(consumer.data.value == 92)
    scenario.verify(consumer.data.currencyPair == "USDEUR")
