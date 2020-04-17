# OrO Node

A simple oracle server to provide off-chain data on tezos blockchain.

## Basic Terminology

### OrO Node
It is used to timely add/update data in your OrO contract(s). 
You can make changes into its configurations and decide how it works and what data it serves to client contract(s)

### OrO Contract
A contract which serves data to client contract(s). Suppose a client contract want to live score. It will query that data from OrO contract by sending the name of match something like INDvsNZ and OrO contract will revert the data to client's entrypoint with requested data. 

### Client Contract
A contract which uses OrO contract data to run a business use case. A client contract can get data from oracle contract by paying some Tezzies.


## Procedure

1. To run OrO node and to consume data from Oro Node using a client contract you have to deploy OrO Contract. Sample OrO contracts are under **[oro-contract][oro-contract]** folder.
2. Once your OrO contract is deployed, you can feed data points using OrO Node provided by tezsure.
3. Once the OrO node is successfully running, anyone can with a client contract can consume relevant data from OrO contract.
4. A client contract should have **'recieveDataFromOrO'** entrypoint to receive data from OrO contract. Sample client contracts are under **client-contract** folder.
5. While deploying client contract make sure you have given correct OrO contract’s address and provide your client some tez which can be used to pay to OrO contract as fee. Default fee is set to 3000 mutez in OrO contract.
6. Test the client contract by sending the requesting your entrypoint to fetch data from OrO contract.

## Getting Started

This project is intended to be used with the latest Active LTS release of [Node.js][nodejs] .

### Clone repository

To clone the repository use the following commands:

```sh
git clone https://github.com/Tezsure/OrO.git
cd OrO
npm install
```

### Deploy OrO contract
Sample OrO contracts for weather data and currency conversion are under **[oro-contract][oro-contract]** folder.

To deploy a **weather OrO contract**, change **CONTRACT_OWNER** value under **deployOrOContract.js**. Also provide relevant keys for the contract owner. 
Use following command to deploy OrO contract. 
```
npm run deploy-oro-contract
```

### Configure OrO Node

+ ##### Edit Tezos Configuration

```json
{
      "tezosConfig":{
         "nodeAddress":"ADDRESS-WHERE-YOU-ARE-GOING-TO-DEPLOY YOUR-SMART-CONTRACT",
         "publicKey":"PUBLIC-KEY-WHICH-WILL-BE-USED-TO-SEND-TRANSACTION-TO-BLOCKCHAIN",
         "privateKey":"PRIVATE-KEY-WHICH-WILL-BE-USED-TO-SEND-TRANSACTION-TO-BLOCKCHAIN",
         "keyHash":"KEY-HASH-WHICH-WILL-BE-USED-TO-SEND-TRANSACTION-TO-BLOCKCHAIN",
         "conseilServerAddress":"CONSEIL-SERVER-ADDRESS",
         "conseilServerAPIKEY":"API-KEY-FROM-NAUTILAS-CLOUD",
         "conseilServerNetwork":"NETWORK-NAME FOR EXAMPLE (carthagenet)"
      }
   }
```
You can use https://testnet.tezster.tech which is a Tezos carthagenet node.

A Tezos node allows you deploy contract, make transaction etc 
Other Tezos Node
+ https://tezos-dev.cryptonomic-infra.tech
+ https://carthagenet.SmartPy.io
+ http://carthagenet.tezos.cryptium.ch:8732

Conseil node is used to access conseil services and you need a API Key for that
+ https://conseil-dev.cryptonomic-infra.tech:443/

Use https://nautilus.cloud to access API KEY for Conseil node.
Use https://faucet.tzalpha.net/ to obtain keys for any testing.
You can use http://smartpy.io/dev/faucetImporter.html to activate the keys obtained from faucet.

#### Edit API Configuration

You can add as many as endpoints you want to Oracle adapter. You need to configure the endpoints carefully.


 
#### Weather Data example

Now in this example we assume that we have four fields which we wish to feed namely city, temprature, pressure and humidity.
For each city you need to get data through some APIs.

Now city is a **fixed** data whereas temprature, humidity and pressure are changing or **custom** data point.


You can configure an adapter for this as shown below.
```json
{
      "endPointsConfig":[
         {
            "entryPointMichelson":"(Left (Pair (Pair 'city' temperature) (Pair pressure humidity)))",
            "contractAddress":"KT1-OrO-Contract-Address",
            "link":"https://api.weatherstack.com/current?access_key=API_KEY&query=Pondicherry",
            "fields":[
               {
                  "type":"fixed",
                  "nameInEntryPoint":"city",
                  "data":"Pondicherry"
               },
               {
                  "type":"custom",
                  "nameInEntryPoint":"temperature",
                  "path":"current.temperature",
                  "isString":false,
                  "doFloor":true,
                  "doCeil":false,
                  "multiplier":1
               },
               {
                  "type":"custom",
                  "nameInEntryPoint":"pressure",
                  "path":"current.pressure",
                  "isString":false,
                  "doFloor":true,
                  "doCeil":false,
                  "multiplier":1
               },
               {
                  "type":"custom",
                  "nameInEntryPoint":"humidity",
                  "path":"current.humidity",
                  "isString":false,
                  "doFloor":true,
                  "doCeil":false,
                  "multiplier":1
               }
            ]
         }]
}
```
The adapter will convert the michelson to some like this while making transaction to blockchain.
```log
(Left (Pair (Pair "Pondicherry" 31) (Pair 1007 51)))
```

All the data points which are treated as a string in Michelson should be enclosed in single quotes ('city') while data types such as integer are treated as number and there's no need to enclose it in single quotes.

#### Currency Data example 

Now in this example we assume that we have two fields which we wish to feed namely conversion key and value.
For each conversion you need to get data through some APIs.

Now conversion key is a **fixed** data whereas value is **custom** or changing data point.

```json
{
      "endPointsConfig":[
         {
            "entryPointMichelson":"(Right (Pair 'key' value))",
            "contractAddress":"KT1-OrO-Contract-Address",
            "link":"https://prime.exchangerate-api.com/v5/API_KEY/latest/USD",
            "fields":[
               {
                  "type":"fixed",
                  "nameInEntryPoint":"key",
                  "data":"USD_INR"
               },
               {
                  "type":"custom",
                  "nameInEntryPoint":"value",
                  "path":"conversion_rates.INR",
                  "isString":false,
                  "doFloor":true,
                  "doCeil":false,
                  "multiplier":100
               }
            ]
         }]
}
```
The adapter will convert the michelson to some like this while making transaction to blockchain.
```log
(Right (Pair "USD_INR" 7645))
```
**multiplier** will change value 76.453 to 7645.3 and **doFLoor** will change the value to 7645. 
By using this configuration, you can achieve the precesion you want for different data points.

#### How can different types of data co-exist in same OrO node ?
As we have discussed example of weather and currency OrO let us show you how can they coexist.

```json
[
   {
      "tezosConfig":{
         "nodeAddress":"",
         "publicKey":"",
         "privateKey":"",
         "keyHash":"",
         "conseilServerAddress":"",
         "conseilServerAPIKEY":"",
         "conseilServerNetwork":""
      }
   },
   {
      "endPointsConfig":[
         {
            "entryPointMichelson":"(Left (Pair (Pair 'city' temperature) (Pair pressure humidity)))",
            "contractAddress":"KT1-OrO-Contract-Address",
            "link":"http://api.weatherstack.com/current?access_key=API_KEY&query=Pondicherry",
            "fields":[
               {
                  "type":"fixed",
                  "nameInEntryPoint":"city",
                  "data":"Pondicherry"
               },
               {
                  "type":"custom",
                  "nameInEntryPoint":"temperature",
                  "path":"current.temperature",
                  "isString":false,
                  "doFloor":true,
                  "doCeil":false,
                  "multiplier":1
               },
               {
                  "type":"custom",
                  "nameInEntryPoint":"pressure",
                  "path":"current.pressure",
                  "isString":false,
                  "doFloor":true,
                  "doCeil":false,
                  "multiplier":1
               },
               {
                  "type":"custom",
                  "nameInEntryPoint":"humidity",
                  "path":"current.humidity",
                  "isString":false,
                  "doFloor":true,
                  "doCeil":false,
                  "multiplier":1
               }
            ]
         },
         {
            "entryPointMichelson":"(Right (Pair 'key' value))",
            "contractAddress":"KT1-OrO-Contract-Address",
            "link":"https://prime.exchangerate-api.com/v5/API_KEY/latest/USD",
            "fields":[
               {
                  "type":"fixed",
                  "nameInEntryPoint":"key",
                  "data":"USD_INR"
               },
               {
                  "type":"custom",
                  "nameInEntryPoint":"value",
                  "path":"conversion_rates.INR",
                  "isString":false,
                  "doFloor":true,
                  "doCeil":false,
                  "multiplier":1
               }
            ]
         }
      ]
   }
]
```
You can add as many configuration as you want to handle different variety of data on your oracle node.

If you want to format string data with some prefix and/or prefix, you can have the below config.

```json
{
   "type":"custom",
   "nameInEntryPoint":"",
   "path":"",
   "isString":true,
   "prefix":"",
   "suffix":""
}
```
### Start the OrO Node
Run
```bash
npm run oro
```

##### Available Scripts
+ `clean` - remove coverage data and transpiled files,
+ `build` - transpile TypeScript to ES6,
+ `build:watch` - interactive watch mode to automatically transpile source files,
+ `lint` - lint source files and tests

### Develop and deploy client contract and test your Oracle
Sample client contracts for weather data and currency conversion are under **[client-contract][client-contract]** folder.
A client contract should have **'recieveDataFromOrO'** entrypoint to receive data from OrO contract.
Here is a smartpy snippet for reference. [Smartpy][smartpy]

Weather Data

```python
@sp.entry_point   
def recieveDataFromOrO(self,params):
 self.data.temprature = params.temprature #of the type sp.TInt
 self.data.pressure = params.pressure #of the type sp.TInt
 self.data.humidity = params.humidity #of the type sp.TInt
```
Currency Data

```python
@sp.entry_point   
def recieveDataFromOrO(self,params):
 self.data.convkey = params.temprature #of the type sp.TString
 self.data.value = params.value #of the type sp.TInt
```

Below script is important for the client contract if you wish to customise client contract.

Weather Data 
```python
contract = sp.contract(sp.TRecord(city = sp.TString), params.address,entry_point="getDataFromOrO").open_some()
requestData = sp.record(city = params.city)
sp.transfer(requestData, sp.mutez(3000), contract)
```
Currency Data
```python
contract = sp.contract(sp.TRecord(convkey = sp.TString), params.address,entry_point="getDataFromOrO").open_some()
requestData = sp.record(convkey = params.convkey)
sp.transfer(requestData, sp.mutez(2000), contract) 
```

#### Understanding **fields** types

In config a field can be of two types.

##### Fixed 

Implies that this data doesn't change over the time. It's used as it is while pushing data to OrO contract.

 + **nameInEntryPoint** is the name of the data point in the provided michelson.
 + **data** is the data which you want to feed in place of that data point.
```json
{
    "type":"fixed",
    "nameInEntryPoint":"",
    "data":""
}
```
##### Custom
A custom data is the data which we get from API. It can be of two types string and integer

###### String

 + **nameInEntryPoint** is the name of the data point in the provided michelson.

 + **path** is the path at which data is present in JSON.

 + **isString** is a boolean (true/false) which is use to specify whether data is a string or not.

 + **prefix** is used if you want to prepand some text to a string while it is being sent to OrO contract.

 + **suffix** is used if you want to append some text to a string before sending it to OrO contract.
 
+ **doFloor** is a boolean (true/false) which tells adapter whether to take floor or not on incoming data.

+ **doCeil** is a boolean (true/false) which tells adapter whether to take ceil or not on incoming data.

+ **multiplier** multiplies the number with incoming data, if you wish to divide you can provide 0.1 or something like that.

+ ##### Integer
    For Tezos contracts, float data type is not supported. If incoming data is float it should be converted to integer before invokation operation using multiplier and doFloor/doCeil configuration.


    ```json
    {
       "type":"custom",
       "nameInEntryPoint":"",
       "path":"",
       "isString":true,
       "prefix":"",
       "suffix":"",
       "doCeil" : false,
       "doFloor" : false,
       "multiplier": 1
    }
    ```


## Future Development
We'll be adding some new set of features to provide more customisation to OrO Node, stay tuned!

## License
Licensed under the MIT. See the [LICENSE](https://github.com/Tezsure/OrO/blob/master/LICENSE) file for details.

[nodejs]: https://nodejs.org/dist/latest-v12.x/docs/api/
[smartpy]: https://smartpy.io/dev/
[client-contract]: https://github.com/Tezsure/OrO/tree/master/client-contract
[test]: https://github.com/Tezsure/OrO/tree/master/test
[oro-contract]: https://github.com/Tezsure/OrO/tree/master/oro-contract
