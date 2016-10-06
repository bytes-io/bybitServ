from bitcoin import *
# import jsonConn
'''
A suite of functions for making manipulating bitcoin more smoothly.
Dependency: pybitcointools library.
'''

# signs all inputs of a tx
def signAllIns(aTx, priv, nbIns=None):
	signedTx = aTx
	utxo = nbIns

	if utxo == None:
		utxo = len(unspent(privtoaddr(priv)))

	for i in range(utxo):
		signedTx = sign(signedTx, i, priv)
	return signedTx

# > PAYMENT
def makePtx(uKeyClient, uKeyServer, toServer):
	script = mk_multisig_script(uKeyClient,uKeyServer,2,2)
	addrServer = pubtoaddr(uKeyServer)
	addrClient = pubtoaddr(uKeyClient)
	outs = [{'value':toServer, 'address':addrServer}]
	histScript = unspent(scriptaddr(script))
	tx = mksend(histScript, outs, addrClient, feeCalculator(histScript))
	return tx

def signAndCombine(aPtx, uKeyClient, sigClient, rKeyServer):
	script = mk_multisig_script(uKeyClient, privtopub(rKeyServer), 2, 2)
	sigServer = multisign(aPtx, 0, script, rKeyServer)
	return apply_multisignatures(aPtx, 0, script, [sigClient, sigServer])

# > DEPOSIT
def expressTx(anAddr, aDst, amnt):
	outs = [{'value': amnt, 'address' : aDst}]
	return mksend(unspent(anAddr), outs, anAddr, 15000)

def expressStx(aPriv, aDst, amnt):
	src = privtoaddr(aPriv)
	tx = expressTx(src, aDst, amnt)
	return signAllIns(tx, aPriv, len(unspent(src)))

def makeDtx(rKeyClient, uKeyServer, dep):
	addrClient = privkey_to_address(rKeyClient)
	utxoClient = unspent(addrClient)

	# Create Script
	pubs = []
	pubs.append(privtopub(rKeyClient))
	pubs.append(uKeyServer)
	script = mk_multisig_script(pubs[0],pubs[1],2,2)  # keys, req, total
	depositAddr = scriptaddr(script)
	histDeposit = history(depositAddr)
	if histDeposit != []:
		print 'Issue with depositAddr: non-void history.'

	# Prepare the DEPOSIT transaction
	outs = [{'value':dep, 'address':depositAddr}]
	tx = mksend(utxoClient, outs, addrClient, feeCalculator(utxoClient))

	# Return
	return [tx, script]

def setTimelock(aTx,locktime):
	dTx=deserialize(aTx)
	dTx['locktime'] = locktime
	# to do (extension): sequence number
	return serialize(dtx)

# Public key exchange
def exchangePubKey(ownKey, connection):
	print "Public key exchange"
	connection.jsend(ownKey)
	out = connection.jrecv()
	return out

# Available balance of an address
def balanceAddr(address):
        avlb = sum(multiaccess(unspent(address),'value'))
        return avlb

# STUB - Optimal fee for given inputs  (arg1) and urgency level (arg2) in 1-3
def feeCalculator(ins, urgent=0):
	if urgent==1:
		return 40000
	return 23000
	# get size in bytes
	# multiply this by current price per byte from https://bitcoinfees.21.co/#delay corresponding to the level of urgency. use curl here. Firewall should allow it.
	# instead of multoplying (this multiplicative perhaps does not reflect the mining market works), estimate function
	# return fee
