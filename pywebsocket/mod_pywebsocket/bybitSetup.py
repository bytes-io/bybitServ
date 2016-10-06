# Author: Samuel Martinet
# Date: 19.8.2016
import hpUtils

# First, forbid all forwarding
# set default policy of FORWARD to drop
hpUtils.setChainPolicy('FORWARD','DROP')
# flush FORWARD
hpUtils.flushChain('FORWARD')
# authorize interaction with blockchain.info
hpUtils.allowSpecificWebsite('104.16.54.3')
hpUtils.allowSpecificWebsite('104.16.55.3')

print('Done with Iptables setup')

# Second, start the server: python mod_pywebsocket/standalone.py -p 7878  -d example
