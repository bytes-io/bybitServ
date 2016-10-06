from bitcoin import *
from pprint import *




def balanceAddr(address):
        avlb = sum(multiaccess(unspent(address),'value'))
        return avlb

fee = 13333
increment = 25000



privClient = 'Kxz9ftuoEVV67eKrUqkz1dnCcCLbDL13HJnP7vX37qQVGy8WPqg1'
privServer = 'L4hdBFMfqYBP7XB9teoiwKTNZq9LoJRfJYtiFTxyHMt74MX97c4X'

pubClient = '034978e3abda7c63510f598edacbc0aa69d346a891c779b1b7a5bbe4cf488ecb7c'
if pubClient != privtopub(privClient) : print "pb with server's public key"
pubServer = '02e4e7fa83a6c014cf005e0773bcfd02db1095a72d12df597a34a655e2e9cc6ab7'
if pubServer != privtopub(privServer) : print "pb with server's public key"

sharedClient = '3Hz4huQypNdjtwKjdvL6XiVbVzmDasG8rm'
scriptServer = mk_multisig_script([pubServer, pubClient], 2,2)
sharedServer = scriptaddr(scriptServer)
if sharedClient != sharedServer: print 'scripts not same'

# print sharedServer


amount = 25000
scriptAddr = bitcoin.scriptaddr(pubArr[1])
print scriptAddr
outs = [{'value': amount, 'address': addressServer}, {'value': (txUtils.balanceAddr(scriptAddr)-amount-feeAmnt), 'address': bitcoin.pubtoaddr(pubArr[0])}]
payment = bitcoin.mktx(bitcoin.unspent(scriptAddr), outs)
sigServer = bitcoin.multisign(payment, 0, pubArr[1], privatekeyServer)
sigclient = msg +'01'
signedPayment = bitcoin.apply_multisignatures(payment, 0, pubArr[1], [sigServer, sigclient])
bitcoin.pushtx(signedPayment)








# tx = '010000000118e52fbc8bc46170483f42746e54684acaac71455af7f72ed88459a4c73a00c600000000490047522102e4e7fa83a6c014cf005e0773bcfd02db1095a72d12df597a34a655e2e9cc6ab721034978e3abda7c63510f598edacbc0aa69d346a891c779b1b7a5bbe4cf488ecb7c52aeffffffff02a8610000000000001976a9144c1ced6e542557a8c577871e313a073f38a9ef2a88acba0a0800000000001976a91460847dd531231442dee31e8dd619f2e892d46c9088ac00000000'

# sigClient = '3045022100c068aae872cc2eb8be8080616ea1972b339565e5c453cb19cfe447d47b99875c02201aefcb37871d4b4a516970560ec69a7b74269a5fc5a823436618540316317a9e'
# sigServer = multisign(tx, 0, scriptServer, privServer)
# print sigServer
# print sigClient
# if verify_tx_input(tx, 0, scriptServer, sigClient, pubClient) != True: print 'Problem with the sig from client'
# if verify_tx_input(tx, 0, scriptServer, sigServer, pubServer) != True: print 'Problem with the sig from server'
# signedSpendTx = apply_multisignatures(tx, 0, scriptServer, [sigServer,sigClient])



# outs = [{'value': increment, 'address': pubtoaddr(pubServer)}, {'value': (balanceAddr(sharedServer)-increment-fee), 'address': pubtoaddr(pubClient)}]
# spendTx = mktx(unspent(sharedServer), outs)
# sigServer = multisign(spendTx, 0, scriptServer, privServer)
# # sigClient2 = multisign(spendTx, 0, scriptServer, privClient)
# sigClient2 = '304402204dae851c29a117383c5c535086a7fe899c9c5f0d927a4e680498fdd9b244cb15022058fea40a9f8c3988b17556fceacdce063860057fd8c6ad84de40515d287758dd01'
# spendTxSigned = apply_multisignatures(spendTx, 0, scriptServer, [sigServer, sigClient2])
# # print sigClient2
# print scriptServer
# print spendTx
# # pushtx(spendTxSigned)
# # if spendTx != tx :
# #     print 'problem with the built of the transactions'
# #     print tx
# #     sigClient2 = multisign(spendTx, 0, scriptServer, privClient)
# #     spendTxSigned = apply_multisignatures(spendTx, 0, scriptServer, sigClient2)
# #     print spendTx
# #     print spendTxSigned
# #
# # 304402204dae851c29a117383c5c535086a7fe899c9c5f0d927a4e680498fdd9b244cb15022058fea40a9f8c3988b17556fceacdce063860057fd8c6ad84de40515d287758dd01
# # 304402204dae851c29a117383c5c535086a7fe899c9c5f0d927a4e680498fdd9b244cb15022058fea40a9f8c3988b17556fceacdce063860057fd8c6ad84de40515d287758dd
# # 01000000016fef96e7a61a3445baa26ce0a2aa147d2a6ffb466932141a081b28522476f73300000000da00483045022100d305e06aef4bf59525462b217982014fab512758ece10428f552a7d2c61dd3ea0220664c4a4afb53d4cf625a1830b27d1725d454afa0c2c0c1d5ae5f112ddb8553a10147304402204dae851c29a117383c5c535086a7fe899c9c5f0d927a4e680498fdd9b244cb15022058fea40a9f8c3988b17556fceacdce063860057fd8c6ad84de40515d287758dd0147522102e4e7fa83a6c014cf005e0773bcfd02db1095a72d12df597a34a655e2e9cc6ab721034978e3abda7c63510f598edacbc0aa69d346a891c779b1b7a5bbe4cf488ecb7c52aeffffffff02a8610000000000001976a9144c1ced6e542557a8c577871e313a073f38a9ef2a88ac72e30400000000001976a91460847dd531231442dee31e8dd619f2e892d46c9088ac00000000
# # 01000000016fef96e7a61a3445baa26ce0a2aa147d2a6ffb466932141a081b28522476f73300000000da00483045022100d305e06aef4bf59525462b217982014fab512758ece10428f552a7d2c61dd3ea0220664c4a4afb53d4cf625a1830b27d1725d454afa0c2c0c1d5ae5f112ddb8553a10147304402204dae851c29a117383c5c535086a7fe899c9c5f0d927a4e680498fdd9b244cb15022058fea40a9f8c3988b17556fceacdce063860057fd8c6ad84de40515d287758dd0147522102e4e7fa83a6c014cf005e0773bcfd02db1095a72d12df597a34a655e2e9cc6ab721034978e3abda7c63510f598edacbc0aa69d346a891c779b1b7a5bbe4cf488ecb7c52aeffffffff02a8610000000000001976a9144c1ced6e542557a8c577871e313a073f38a9ef2a88ac72e30400000000001976a91460847dd531231442dee31e8dd619f2e892d46c9088ac00000000
#
# # sig = multisign(spendTx, 0, script, privKey)
# # sigServer= multisign(spendTx, 0, script, privKeyServer)
# # #signedSpendTx = apply_multisignatures(spendTx, 0, script, [sig, sigServer])
# # signedSpendTx = apply_multisignatures(spendTx, 0, script, [sigServer,sig])
# #
# # print 'SpendTx: ', spendTx
# # print 'SignedSpendTx: ', signedSpendTx
#
#
#
#
#
#
#
#
#
# # def balanceAddr(address):
# #         avlb = sum(multiaccess(unspent(address),'value'))
# #         return avlb
# # '''
# #  2 strategies:
# #  - mirror
# #  - inter-feed
# # '''
# # # Set-up
# # privKey = 'KyLuCNsxddnqpdJW1Q3q2mQtkssThJUfcGq9hdCE8W72xYPD3He3'
# # privKeyServer = 'L4hdBFMfqYBP7XB9teoiwKTNZq9LoJRfJYtiFTxyHMt74MX97c4X'
# # pubKey = privtopub(privKey)
# # pubKeyServer = privtopub(privKeyServer)
# # addr = pubtoaddr(pubKey)
# # addrServer = pubtoaddr(pubKeyServer)
# # depositAmount = 80000
# # incrementAmount = 15000
# # feeAmount = 13333
# #
# # # # Funding
# # # #script = mk_multisig_script([pubKey, pubKeyServer], 2,2) // invert it!
# # script = mk_multisig_script([pubKeyServer, pubKey], 2,2)
# # # scriptAddr = scriptaddr(script)
# # #
# # # print 'Script: ',script
# # # print 'ScriptAddr: ',scriptAddr
# # #
# # # output = [{'value': depositAmount, 'address': addrServer}]
# # # fundTx = mksend(unspent(addr), output, addr, feeAmount)
# # #
# # # print 'Funding tx: ', fundTx
# # # fundTx = '0100000002d023b49605aa091f76ba1835d2807e31e31f5117776e330f4a351e252d18b83a010000006b483045022100e5735fa87377557c6417b5a05e130af12b7aba19cd623f4cca63c2f64482e6cd02207a3b9018d06f8b6022a0b60b7fd65cc780e951d3daa8375080d07e68344bd3a70121034cbddad6d4ffbdfba801cf88c05396eb0b6485bf9fa4adba44e260019ce8aa6affffffffb56fd65616a29b1b8dbf361b81ddfdc9ead569e23aac9ba46298293f275ee228010000006a47304402201eb8137f64fbd8cd9ffac58a63c81ffbb8ce8aed17f6df9e30970ae41c7d89700220798026216da9469d91f770e1c3be59df546899e1f96f564c34b0c2dcacce636c0121034cbddad6d4ffbdfba801cf88c05396eb0b6485bf9fa4adba44e260019ce8aa6affffffff011f0301000000000017a91421b78a696fec3349fb626b83bb960d74e7e8e9518700000000'
# # # signedFundTx = sign(fundTx, 0, privKey)
# # # print signedFundTx
# # # pushtx(signedFundTx)
# #
# # # # spending
# # # outs = [{'value': depositAmount, 'address': addrServer}, {'value': (balanceAddr(scriptAddr)-depositAmount-10000), 'address': addr}]
# # # spendTx = mktx(unspent(scriptAddr), outs)
# # spendTx= '010000000184a1122eed4cee5de99ffbe0aadd614283bbe9b3494932e66734e61c99d633dd00000000490047522102e4e7fa83a6c014cf005e0773bcfd02db1095a72d12df597a34a655e2e9cc6ab721034cbddad6d4ffbdfba801cf88c05396eb0b6485bf9fa4adba44e260019ce8aa6a52aeffffffff02983a0000000000001976a9144c1ced6e542557a8c577871e313a073f38a9ef2a88ac72940000000000001976a9147a5dd8777870e667f108de0ac50127b5bd29d2ff88ac00000000'
# # sig = multisign(spendTx, 0, script, privKey)
# # sigServer= multisign(spendTx, 0, script, privKeyServer)
# # #signedSpendTx = apply_multisignatures(spendTx, 0, script, [sig, sigServer])
# # signedSpendTx = apply_multisignatures(spendTx, 0, script, [sigServer,sig])
# #
# # print 'SpendTx: ', spendTx
# # print 'SignedSpendTx: ', signedSpendTx
#
#
# Unsigned Tx pybitcointools:
# 01000000016fef96e7a61a3445baa26ce0a2aa147d2a6ffb466932141a081b28522476f7330000000000ffffffff02a8610000000000001976a9144c1ced6e542557a8c577871e313a073f38a9ef2a88ac72e30400000000001976a91460847dd531231442dee31e8dd619f2e892d46c9088ac00000000
# Script:
# 522102e4e7fa83a6c014cf005e0773bcfd02db1095a72d12df597a34a655e2e9cc6ab721034978e3abda7c63510f598edacbc0aa69d346a891c779b1b7a5bbe4cf488ecb7c52ae
#
# Unsigned Tx bitcore-lib:
# 01000000016fef96e7a61a3445baa26ce0a2aa147d2a6ffb466932141a081b28522476f73300000000490047522102e4e7fa83a6c014cf005e0773bcfd02db1095a72d12df597a34a655e2e9cc6ab721034978e3abda7c63510f598edacbc0aa69d346a891c779b1b7a5bbe4cf488ecb7c52aeffffffff02a8610000000000001976a9144c1ced6e542557a8c577871e313a073f38a9ef2a88ac72e30400000000001976a91460847dd531231442dee31e8dd619f2e892d46c9088ac00000000
#
