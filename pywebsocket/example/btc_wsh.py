''' IMPORTS
'''
# standard imports:
from threading import Thread
import sys
import thread
from time import sleep
# own imports:
import bitcoin
import hpUtils, txUtils

''' PARAMETERS & GLOBAL VARIABLES
'''
clients = []
_GOODBYE_MESSAGE = u'Goodbye'

pricePerKbit= 8000
noKbits = 1
feeAmnt = 23333

privatekeyServer = 'KwiEJGg6dWFLNTVThEjfLVNweWc3rnVCUqfP1h9YDPPUm2Godhir'
pubKeyServer =  bitcoin.privtopub(privatekeyServer)
addressServer = bitcoin.privtoaddr(privatekeyServer)

increment = pricePerKbit*noKbits
paymentNo = []
paymentNo.append(0)

privClient = 'KxoJnYmWujyrL3evv1L2wqzXvovQG1P59Gfcrn9Mx7mt1eFnVEMW'

def web_socket_do_extra_handshake(request):
    # This example handler accepts any request. See origin_check_wsh.py for how
    # to reject access from untrusted scripts based on origin value.
    pass  # Always accept.

################################################################################

''' CLASS DEFINITIONS
'''
class controller(Thread):
    '''
    This class monitors the client's consumption of internet and enforces some
    business rules on the network reflecting who is entitled to access the internet
    or not. It runs on its own thread for security reasons.
    '''
    def __init__(self, info, priv, pubC = None):
        Thread.__init__(self)
        self.pubKeyClient = pubC        # public key of the client
        self.privS = priv            # private key of the server
        self.usage = 0              # bandwidth used by client
        self.balance = 300000       # initial balance
        self.ipClient = info
        self.finishing = False
        self.lastpayment = None   # last payment received from client
        self.lastsig= None      # corresponding signature

    def notify(self, payment, signature, amnt):
    # notify the Controller of intercation with a client
        if self.finishing: return
        if payment != None:
            self.lastpayment= payment
        if signature != None:
            self.lastsig = signature
        if amnt != None:
            self.balance += amnt*8

    def pushPayment(self):
    # To be called once client consumed all he had paid for.
        print 'Broadcasting very last payment'
        print self.lastpayment
        bitcoin.pushtx(self.lastpayment)
        print 'Successful. Payment hash: ', bitcoin.txhash(self.lastpayment)

    def controlSpin(self):
        # compares current usage and data allowance
        while True:
            sleep(2)
            # self.balance -= 20000
            print 'Current balance:', self.balance
            print 'Current usage:' , hpUtils.retrieveUsage(self.ipClient)
            if hpUtils.retrieveUsage(self.ipClient) > self.balance:
                print 'Usage exceeds balance => deny Fwd'
                self.finishing = True
                hpUtils.denyFwd(self.ipClient)
                return

    def run(self):
        print 'Controller starts its job'
        # allow the client ot use the internet:
        hpUtils.allowFwd(self.ipClient)
        # starts monitoring the client's consumption:
        self.controlSpin()
        # brodacast payment
        self.pushPayment()
        # terminate
        print 'controller terminating'

def web_socket_transfer_data(request):
    # print 'type: ', type(request)
    # print 'print: ', request
    # print 'dir: ', dir(request)
    # # print 'conn: ', request.connection
    # print 'dir(conn): ', dir(request.connection)
    # print 'clt: ', request.client_terminated
    # request.client_terminated=True
    # print 'clt: ', request.client_terminated
    # print thread.get_indent()
    # print thread.get_ident()
    # clients.append(infoClient)
    phase = 0
    rad = request.connection.get_remote_addr()
    ipClient = rad[0].split(":")[3]
    pubKeyClientArr = []
    contrl = None
    print 'User connected. Assigned IP:', ipClient
    request.ws_stream.send_message(unicode(pricePerKbit), binary=False)
    request.ws_stream.send_message(unicode(pubKeyServer), binary=False)
    sleep(.25)
    while True:
        sleep(.1)
        line=request.ws_stream.receive_message()
        phase = messageClassifer(line,phase, pubKeyClientArr, contrl, paymentNo)
        if (phase == -1):
            print 'Problem!'
        if (phase == 2) and contrl == None:
            contrl = controller(ipClient, privatekeyServer, pubKeyClientArr[0])
            contrl.start()
        if isinstance(line,unicode):
            # request.ws_stream.send_message(line, binary=False)
            if line == _GOODBYE_MESSAGE:
                print 'Goodbye'
                break
        else:
            print 'Communication in Unicode only!'

    print 'web_socket_transfer_data returned'
    return

def checkValidPubKey(msg):
    return True
def checkValidSignedDtx(msg):
    return True
def checkValidPmt(msg):
    return True
def checkValidSig(msg):
    return True

def messageClassifer(msg, phase, pubArr, aController, paymentNo):
    if phase==0:
    	print 'Received public key from client.'
        if not checkValidPubKey(msg): return -1
        pubArr.append(msg)
        pubArr.append(bitcoin.mk_multisig_script(pubKeyServer, pubArr[0],2,2))
        print msg
        print 'Own script:'
        print bitcoin.scriptaddr(pubArr[1])
        phase += 1
    elif phase==1:
        print 'Received signed Dtx'
        if not checkValidSignedDtx(msg): return -1
        print 'Broadcast signed Dtx'
        print msg
        try:
            bitcoin.pushtx(msg)
            print 'successful broadcast Dtx'
        except:
            print 'unsuccessful broadcast Dtx'
    	print 5*'#',' MPC initialised ', 5*'#'
        phase += 1
    elif phase==2:
    	print 'Payment received'
        if not checkValidPmt(msg): return -1
    	# aController.notify(msg,None,None)
        phase += 1
        paymentNo[0] += 1
    elif phase==3:
    	print 'Signature received'
        if not checkValidSig(msg): return -1
        phase -= 1

        amount =  paymentNo[0] * increment
        scriptAddr = bitcoin.scriptaddr(pubArr[1])
        #printffff 'scriptAddr: ', scriptAddr
        outs = [{'value': amount, 'address': addressServer}, {'value': (txUtils.balanceAddr(scriptAddr)-amount-feeAmnt), 'address': bitcoin.pubtoaddr(pubArr[0])}]
        # prinffffffft 'outs: ', outs
        payment = bitcoin.mktx(bitcoin.unspent(scriptAddr), outs)
        print 'Payment: ', payment
        sigServer = bitcoin.multisign(payment, 0, pubArr[1], privatekeyServer)
        # print 'sigC: fffffffffff', sigServer
        sigClient = msg +'01'
        print 'Sig Client: ', sigClient
        # print bitcoin.multisign(payment, 0, pubArr[1], privClient)
        signedPayment = bitcoin.apply_multisignatures(payment, 0, pubArr[1], [sigServer, sigClient])
        aController.notify(signedPayment, None, 23777)
        # print 'signedPayment: ', signfffffffffffedPayment
        # if pafffffffymentNo[0] == 3: aController.pushPayment()
        # if paymentNoffffffff[0] == 3: bitcoin.pushtx(signedPayment)
        # print 'ALLGOOOD!'
    return phase
