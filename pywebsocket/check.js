/*
Dependencies: bitcore (global), unirest (almost global),
>> check taht unirest and bitcore-lib are front-end compatible
// browsify to compile
> bluebird - is a promise library
> unirest - is a http request
> JQUERY deferred vs. promise
> management of asynchronicity
Primise.each(<iterator>, (returns a promise))
*/

// DEPENDENCIES
var btc = require('bitcore-lib')
var unirest = require('unirest')

// CONSTANTS AND PARAMETERS
var privKey = new btc.PrivateKey.fromWIF('KxoJnYmWujyrL3evv1L2wqzXvovQG1P59Gfcrn9Mx7mt1eFnVEMW')

// 1CA1rufdFggCkd4kZQaff6NxZa1P9AfrrE
var pubKey = privKey.toPublicKey()
var addr = pubKey.toAddress(btc.Networks.livenet)
var pubKeyServer;
var pricePerKbit;
var phase = 0
var depositAmnt;
var incrementAmnt = 500
var feeAmnt = 23333
var scriptAddr;
var pubKeyServer = btc.PublicKey('02e4e7fa83a6c014cf005e0773bcfd02db1095a72d12df597a34a655e2e9cc6ab7')
// HELPER FUNCTIONS:
function getBalanceAddr(anAddr){
  return new Promise(function(resolve, reject) {
    request = 'https://blockchain.info/rawaddr/' + anAddr + '?&limit=0'
    // console.log(request)
    unirest.get(request)
    .end(function(response) {
      resolve(response.body.final_balance) // no reject here !! Todo.
    })
  })
}
function HTTPtoUTXO(response, anAddr){
  // Process the result of http request to blockchain.info into bitcore's UTXO object format
  var body = response.body;
  var utxosRaw = body["unspent_outputs"]
  var UTXOs = []
  utxosRaw.forEach(function(elem){
    var utxo = new btc.Transaction.UnspentOutput({
      "txId" : elem.tx_hash_big_endian,
      "outputIndex" : elem.tx_output_n,
      "address" : anAddr,
      "script" : elem.script,
      "satoshis" : elem.value })
    UTXOs.push(utxo);
  })
  return UTXOs
}
function txPromise(pubkey, toAddr, amount){
  // Return, as a promise, an unigned transaction
  var srcAddr = pubkey.toAddress(btc.Networks.livenet)
  return new Promise(function(resolve, reject) {
    unirest.get('https://blockchain.info/unspent?cors=true&active=' + srcAddr)
    .end(function(response) {
      var UTXOs = HTTPtoUTXO(response, srcAddr)
      // console.log('Utxos retrieved and processed:', UTXOs)
      var transaction = new btc.Transaction()
        .from(UTXOs)
        .to(toAddr, amount)
        .change(srcAddr)
        .fee(feeAmnt)
       resolve(transaction) // no reject here !! Todo.
    })
  })
};
function txFromP2shPromise(pubKey1, pubKey2, amountTo2){
  // Function to automate spending from a P2SH address
  var publicKeys = [pubKey1, pubKey2];
  var scriptAddr = new btc.Address(publicKeys, 2, btc.Networks.livenet)
  var redeemScript = new btc.Script(scriptAddr)
  var addr1 = pubKey1.toAddress().toString();
  var addr2 = pubKey2.toAddress().toString();

  console.log('https://blockchain.info/unspent?cors=true&active='+scriptAddr)
  return new Promise(function(resolve, reject) {
    unirest.get('https://blockchain.info/unspent?cors=true&active=' + scriptAddr)
      .end(function(response) {
        console.log('in')
        var body = response.body;
        var utxosRaw = body["unspent_outputs"]
        // console.log('UtxosRaw: ', utxosRaw)
        var UTXOs = []
        utxosRaw.forEach(function(elem){
          var utxo = new btc.Transaction.UnspentOutput({
            "txId" : elem.tx_hash_big_endian,
            "outputIndex" : elem.tx_output_n,
            "address" : scriptAddr.toString(),
            "script" : elem.script,
            //  "script" : new bitcore.Script(scriptAddr).toHex(), // would not redeemScript work here? How do they go from addr to script
            "satoshis" : elem.value })
          UTXOs.push(utxo);
        })
        var transaction = new btc.Transaction()
          .from(UTXOs, publicKeys, 2)
          .to(addr2, amountTo2)
          .change(addr1)
          .fee(feeAmnt)
        resolve(transaction) // no reject here !! Todo.
      });
  })
};
var privKeyServer = 'KwiEJGg6dWFLNTVThEjfLVNweWc3rnVCUqfP1h9YDPPUm2Godhir'
setTimeout(function(){
    txFromP2shPromise(pubKey, pubKeyServer, incrementAmnt).then(function(out){
      console.log('txFromP2shPromise returned: ', out)
      out.sign([privKeyServer, privKey])
      console.log(out)
      var signature = out.getSignatures(privKey)[0].signature;
      var signatureS = out.getSignatures(privKeyServer)[0].signature;
      console.log(signature.toString())

      // console.log('signature sent: ', signature.toString)
    })
}, 2000)

// console.log('hi')
