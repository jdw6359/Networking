import utils
import time
import logging
import os

def main():
    cellRouterAddress = os.environ['BINARY_CELL_ROUTER_ADDRESS']
    logging.info('cell router address: %s', str(cellRouterAddress))
    logging.info('pinging cell router...%s', str(cellRouterAddress))
    pingResponse = utils.pingAddress(cellRouterAddress)
    if pingResponse == 0:
        logging.info('response from ping: %s', pingResponse)
        cellRouterActive = True
    else:
        logging.warning('no responses from ping to %s', cellRouterAddress)

        print 'write to twitter'

main()