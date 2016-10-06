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
var WebSocket = require('ws');

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
var incrementAmnt = 500
var feeAmnt = 16333
var paymentNo = 0


// HELPER FUNCTIONS:
function disconnect(aWS) { console.log('disconnecting'); aWS.close() }
function getBalanceAddr(anAddr){
  return new Promise(function(resolve, reject) {
    request = 'https://blockchain.info/rawaddr/' + anAddr + '?&limit=0'
    console.log(request)
    unirest.get(request)
    .end(function(response) {
      //resolve(response.body.final_balance) // no reject here !! Todo.
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
function txPromise(_pubkey, toAddr, amount, _fee){
  // Return, as a promise, an unigned transaction
  var srcAddr = _pubkey.toAddress(btc.Networks.livenet)
  return new Promise(function(resolve, reject) {
    var request = 'https://blockchain.info/unspent?cors=true&active=' + srcAddr
    console.log(request)
    unirest.get(request)
    .end(function(response) {
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
    unirest.get(request)
      .end(function(response) {
        var body = response.body;
        var utxosRaw = body["unspent_outputs"]
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

// WEBSOCKET DEFINITION:
getBalanceAddr(addr).then(function(out){
  if (out>20000){
    depositAmnt = out - feeAmnt;
    // console.log(depositAmnt)
    ws= new WebSocket("ws://localhost:7878/btc");

    ws.on('error', function(error){ console.log('Communication problem')})

    ws.onopen = function(e) {
      console.log('Connection to server opened');
      ws.send(pubKey.toString())
    }

    ws.onmessage = function(e) {
      // console.log('msg received!:', e.data)
      if (phase ===0) {
        console.log('price received')
        pricePerKbit = e.data
        phase +=1
        // console.log(pricePerKbit)
      }
      else if (phase === 1) {
        console.log('public key received!')
        pubKeyServer = new btc.PublicKey(e.data)
        phase += 1
        scriptAddr = new btc.Address([pubKey, pubKeyServer],2, btc.Networks.livenet)

        txPromise(pubKey, scriptAddr, depositAmnt, feeAmnt).then(function(out){
          //console.log('Funding tx, UNsigned: ', out)
          out.sign(privKey)
          console.log('Shared Address: ', scriptAddr)
          ws.send(out.toString())
        })

      }
      else if (phase > 1){
        console.log('unexpected message has arrived')
        console.log(e.data)
      }
    }
    ws.onclose = function(e) { console.log("Connection closed") }

  } else {
    console.log('Client has got no money')
  }
  }
)

// MAIN SCRIPT

// while internet access works, pay by interval (or better, adaptive rule)

//
setTimeout(function(){
  setInterval(function(){
    paymentNo += 1
    txFromP2shPromise(pubKey, pubKeyServer, incrementAmnt*paymentNo, feeAmnt).then(function(out){
      // console.log('txFromP2shPromise returned: ', out)
      console.log('Send payment template no.',paymentNo)
      ws.send(out.toString())
      var signature = out.getSignatures(privKey)[0].signature;
      // console.log('signature sent: ', signature.toString())
      console.log('Send associated signature')
      ws.send(signature.toString())
      // out.sign([privKey, privKeyServer])
      // console.log('signedpayment: ',out)
    })
  }, 2000)
}, 3000)

// console.log('hi')
