'''
    command line arguments example
'''

import argparse
import logging
import sys

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    logging.basicConfig(stream=sys.stdout)
    
    logger = logging.getLogger()
    logger.setLevel(level=logging.DEBUG)
 
    logger.info('argument test')
    

    parser.add_argument('-addr', '--address', help='address to connect')
    parser.add_argument('-r','--row',help='row address')
    parser.add_argument('-c','--colum',help='colum address')
    
    args = parser.parse_args()
    
    logger.info(f'parse arg info: address = {args.address}, row = {args.row}, col = {args.colum}')
    pass
        