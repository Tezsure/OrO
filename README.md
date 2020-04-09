# Tezsure-weather-oracle

A simple oracle server to provide weather data on tezos blockchain.

## Basic Terminology

### OrO Node
It is used to timely add/update data in your OrO contract. 
You can make changes into its configurations and decide how it works and what data it serves to client contract

### OrO Contract
A contract which serves data to client contract(s). Suppose a client contract want to access weather data of any city. It will query that data from OrO contract by sending the name of city and OrO contract will revert the data to client's entrypoint with requested data.

### Client Contract
A contract which uses OrO contract data to run a business use case. A client contract can get data from oracle contract by paying some Tez.


## Procedure

1. To run OrO node and to consume data from Oro Node using a client contract you have to deploy OrO Contract.
2. Once your OrO contract is deployed, you can feed data points using OrO Node provided by tezsure.
3. Once the OrO node is successfully running, anyone can with a client contract can consume relevant data from OrO contract.
4. A client contract should have **'recieveDataFromOrO'** entrypoint to receive data from OrO contract. OrO contract sends three integer parameters namely temperature, pressure and humidity. A client contract can have another entry point to fetch data from OrO contract. A sample client contract is under **[client-contract][client-contract]** folder.
5. While deploying client contract make sure you have given correct OrO contract’s address and provide your client some tezzie which can be used to pay to OrO contract as fee. Default fee is set to 3000 tezzie in OrO contract.
6. Test the client contract by sending the requesting your entrypoint to fetch data from OrO contract.

## Getting Started

This project is intended to be used with the latest Active LTS release of [Node.js][nodejs] .

### Clone repository

To clone the repository use the following commands:

```sh
git clone https://github.com/Tezsure/tezsure-weather-oracle
cd tezsure-weather-oracle
npm install
```


### Develop and deploy OrO contract

A Weather Oracle contract is provided under **[oro-contract][oro-contract]** directory.
Change **CONTRACT_OWNER** value under **deployOrOContract.js**. Also provide relevant keys for the contract owner.
Use following command to deploy OrO contract. 
```
npm run deploy-oro-contract
```
If you wish to customise OrO contract, you can use provided template to do so. [Smartpy][smartpy]

### Configure Weather OrO Node

+ ##### Edit Tezos Configuration

```json
{
      "tezosConfig":{
         "nodeAddress":"ADDRESS-WHERE-YOU-ARE-GOING-TO-DEPLOY YOUR-SMART-CONTRACT",
         "publicKey":"PUBLIC-KEY-WHICH-WILL-BE-USED-TO-SEND-TRANSACTION-TO-BLOCKCHAIN",
         "privateKey":"PRIVATE-KEY-WHICH-WILL-BE-USED-TO-SEND-TRANSACTION-TO-BLOCKCHAIN",
         "keyHash":"KEY-HASH-WHICH-WILL-BE-USED-TO-SEND-TRANSACTION-TO-BLOCKCHAIN",
         "contractAddress":"KT1-ADDRESS-OF-THE-CONTRACT",
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

Conseil Node is used to access conseil services and you need a API Key for that
+ https://conseil-dev.cryptonomic-infra.tech:443/

Use https://nautilus.cloud to access API KEY for Conseil node.
Use https://faucet.tzalpha.net/ to obtain keys for any testing.
You can use http://smartpy.io/dev/faucetImporter.html to activate the keys obtained from faucet.

+ #### Edit API Configuration

You can add as many cities you want to Oracle adapter. You need to add city name, its API endpoints and response format as shown below.
Our OrO node will average all API data for a city and send it to your Oracle contract.

```json
{
            "City Name 1":[
               {
                  "link":"http://api.weatherstack.com/current?access_key=API_KEY&query=City Name 1",
                  "temperaturePosition":"current.temperature",
                  "tempUnits":"C",
                  "pressurePosition":"current.pressure",
                  "humidityPosition":"current.humidity"
               },
               {
                  "link":"http://api.openweathermap.org/data/2.5/weather?q=City Name 1&APPID=API_KEY",
                  "temperaturePosition":"main.temp",
                  "tempUnits":"K",
                  "pressurePosition":"main.pressure",
                  "humidityPosition":"main.humidity"
               }
            ]
}

```

Please refer test-weather-oro-config.json file under **[test][test]** folder for reference purpose.

### Start the OrO Node
Run
```bash
npm run weather-oro
```

##### Available Scripts
+ `clean` - remove coverage data and transpiled files,
+ `build` - transpile TypeScript to ES6,
+ `build:watch` - interactive watch mode to automatically transpile source files,
+ `lint` - lint source files and tests

### Develop and deploy and client contract and test your Oracle
A sample client contract is under **[client-contract][client-contract]** folder.
A client contract should have **'recieveDataFromOrO'** entrypoint to receive data from OrO contract.
Here is a smartpy snippet for reference. [Smartpy][smartpy]

```python
@sp.entry_point   
def recieveDataFromOrO(self,params):
 self.data.temprature = params.temprature #of the type sp.TInt
 self.data.pressure = params.pressure #of the type sp.TInt
 self.data.humidity = params.humidity #of the type sp.TInt

```

Below script is important for the client contract if you wish to customise client contract.
```python
c = sp.contract(sp.TRecord(city = sp.TString),sp.address("KT1-OrO-Contract-Address"),entry_point="getDataFromOrO").open_some()
requestData = sp.record(city = params.key) # params.key can be like "Bangalore"
sp.transfer(mydata,sp.mutez(3000),c) 
```


## License
Licensed under the MIT. See the [LICENSE](https://github.com/Tezsure/tezsure-weather-OrO/blob/master/LICENSE) file for details.

[nodejs]: https://nodejs.org/dist/latest-v12.x/docs/api/
[smartpy]: https://smartpy.io/dev/
[client-contract]: https://github.com/Tezsure/tezsure-weather-OrO/tree/master/client-contract
[test]: https://github.com/Tezsure/tezsure-weather-OrO/tree/master/test
[oro-contract]: https://github.com/Tezsure/tezsure-weather-OrO/tree/master/oro-contract