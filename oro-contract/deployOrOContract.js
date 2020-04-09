const conseiljs = require('conseiljs');
const fs = require('fs');

const tezosNode = 'https://testnet.tezster.tech';
const CONTRACT_OWNER = 'tz1V8NMNR5LBveuGJYruujnYwgv4tWF1oXZQ';
const CONTRACT_FILE = 'weather-oro.tz.json'

async function deployContract() {
    const data = fs.readFileSync(__dirname + '/' + CONTRACT_FILE , {encoding:'utf8'}); 
  const keystore = {
    publicKey: 'edpkttgvzu7bVqwdz6cWu2CRT4kNjjXKKrfDNTdVrv9Z5LzmNK6Ljm',
    privateKey: 'edskRvTq52CssMWPNNaX5LLFP4rA4WJVeSUTufGpwovrPUF9qwCU9cP3kPFQYHz2YPKBnAcJ9qHKJPRd1hwrFFpAUS2Hr52Eyb',
    publicKeyHash: 'tz1V8NMNR5LBveuGJYruujnYwgv4tWF1oXZQ',
    seed: '',
    storeType: conseiljs.StoreType.Fundraiser
  };

  const storage = `{ "prim": "Pair", "args": [ [], [ { "string": "${CONTRACT_OWNER}" } ] ] }`;
  console.log('Deploying Contract .... ');
  try {
    const result = await conseiljs.TezosNodeWriter.sendContractOriginationOperation(
      tezosNode,
      keystore,
      1000000,
      undefined,
      100000,
      '',
      10000,
      100000,
      data,
      storage,
      conseiljs.TezosParameterFormat.Micheline
    );
  
    console.log(`Injected operation Contract Deployed with group Addr : ${result.results.contents[0].metadata.operation_result.originated_contracts[0]}`);
  } catch(error) {
    console.log(`Error while deploting contract :`);
    console.log(error);
  }
}

deployContract();
