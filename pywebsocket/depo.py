import bitcoin
from time import sleep

privS='KwiEJGg6dWFLNTVThEjfLVNweWc3rnVCUqfP1h9YDPPUm2Godhir'
privC= 'KxoJnYmWujyrL3evv1L2wqzXvovQG1P59Gfcrn9Mx7mt1eFnVEMW'
addrC = bitcoin.privtoaddr(privC)
script = bitcoin.mk_multisig_script(bitcoin.privtopub(privS), bitcoin.privtopub(privC), 2, 2)
addr = bitcoin.scriptaddr(script)
print addr 
#tx  = bitcoin.mksend(bitcoin.unspent(addrC), [{'value': 100000, 'address': addr}], addrC, 20000)


sleep(2)
#tx = bitcoin.sign(tx,0, privC)
#bitcoin.pushtx(tx)  

tx2 = bitcoin.mksend(bitcoin.unspent(addr), [{'value': 75000, 'address': addrC}], addrC, 25000)
sigC = bitcoin.multisign(tx2, 0, script, privC)
sigS = bitcoin.multisign(tx2, 0, script, privS)
tx2  = bitcoin.apply_multisignatures(tx2, 0, script, [sigS, sigC])
try:
  bitcoin.pushtx(tx2) 
except: 
  print 'some exception was raised'
finally:
  print 'finalement'
print 'end'
