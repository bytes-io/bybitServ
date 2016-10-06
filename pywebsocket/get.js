var XMLHttpRequest = require("xmlhttprequest").XMLHttpRequest
var btc = require('bitcore-lib')

// CONSTANTS AND PARAMETERS
var privKey = new btc.PrivateKey.fromWIF('Kxz9ftuoEVV67eKrUqkz1dnCcCLbDL13HJnP7vX37qQVGy8WPqg1')

// 1CA1rufdFggCkd4kZQaff6NxZa1P9AfrrE
var pubKey = privKey.toPublicKey()
var addr = pubKey.toAddress(btc.Networks.livenet)
var pubKeyServer;
var pricePerKbit;
var phase = 0
var ws;
var depositAmnt;
var incrementAmnt = 5000
var feeAmnt = 14333
var paymentNo = 0










function apiPromise(request){
  return new Promise(function(resolve, reject) {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', request);
    xhr.onload = function() {
        if (xhr.status === 200) {
          resolve(JSON.parse(xhr.responseText));
        }
        else {
              console.log('Request failed.  Returned status of ' + xhr.status);
        }
    };
    xhr.send();
  })
}
function getBalanceAddr(anAddr){
  return new Promise(function(resolve, reject) {
    request = 'https://blockchain.info/rawaddr/' + anAddr + '?&limit=0'
    // console.log(request)
    apiPromise(request).then(function(out){
      resolve(out.final_balance) // no reject here !! Todo.
    })
  })
}
function HTTPtoUTXO(response, anAddr){
  // Process the result of http request to blockchain.info into bitcore's UTXO object format

  var utxosRaw = response.unspent_outputs
  var UTXOs = []
  utxosRaw.forEach(function(elem){
    var utxo = new btc.Transaction.UnspentOutput({
      "txId" : elem.tx_hash_big_endian,
      "outputIndex" : elem.tx_output_n,
      "address" : anAddr,
      "script" : elem.script,
      "satoshis" : elem.value })
    UTXOs.push(utxo);
    console.log('ear')
  })
  return UTXOs
}
function txPromise(_pubkey, toAddr, amount, _fee){
  // Return, as a promise, an unigned transaction
  var srcAddr = _pubkey.toAddress(btc.Networks.livenet)
  return new Promise(function(resolve, reject) {
    var request = 'https://blockchain.info/unspent?cors=true&active=' + srcAddr
    apiPromise(request)
    .then(function(response) {
      console.log(response.unspent_outputs)
      var UTXOs = HTTPtoUTXO(response, srcAddr)
      console.log('Utxos retrieved and processed:', UTXOs)
      var transaction = new btc.Transaction()
        .from(UTXOs)
        .to(toAddr, amount)
        .change(srcAddr)
        .fee(_fee)
       resolve(transaction) // no reject here !! Todo.
    })
  })
};
function txFromP2shPromise(pubKey1, pubKey2, amountTo2,_fee){
 // Function to automate spending from a P2SH address
 var publicKeys = [pubKey1, pubKey2];
 var scriptAddr = new btc.Address(publicKeys, 2, btc.Networks.livenet)
 var redeemScript = new btc.Script(scriptAddr)
 var addr1 = pubKey1.toAddress().toString();
 var addr2 = pubKey2.toAddress().toString();
 console.log(redeemScript)

 return new Promise(function(resolve, reject) {
   // console.log('salut')
   var request = 'https://blockchain.info/unspent?cors=true&active=' + scriptAddr
   // console.log(request)
   apiPromise(request)
     .then(function(response) {
       var utxosRaw = response.uns
       // console.log('UtxosRaw: ', utxosRaw)
       var UTXOs = []
       utxosRaw.forEach(function(elem){
         var utxo = new btc.Transaction.UnspentOutput({
           "txId" : elem.tx_hash_big_endian,
           "outputIndex" : elem.tx_output_n,
           "address" : scriptAddr, // .toString() / .toHex() ?
           "script" : elem.script,
           //  "script" : new bitcore.Script(scriptAddr).toHex(), // would not redeemScript work here? How do they go from addr to script
           "satoshis" : elem.value })
         UTXOs.push(utxo);
       })
       var transaction = new btc.Transaction()
         .from(UTXOs, publicKeys, 2)
         .to(addr2, amountTo2)
         .change(addr1)
         .fee(_fee)
       resolve(transaction) // no reject here !! Todo.
     });
 })
};

///////////////////////////////////////////////////////////////////////
adr = '1CDv5AmKZTbYvRVwRXRX4ccbK5Hka3BuaT'
getBalanceAddr(adr).then(function(out){
  console.log(out)
}
)
txPromise(pubKey,adr,10000,10000).then(function(out) {console.log(out)})
