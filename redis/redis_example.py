'''
    redis example
'''

import logging
import sys
import redis
import time

if __name__ == '__main__':
    
    logging.basicConfig(stream=sys.stdout)
    
    logger = logging.getLogger()
    logger.setLevel(level=logging.DEBUG)
 
    logger.info('argument test')
    
    rdconn = redis.Redis(host='localhost', port=6379, db=0)

    logger.info('redis read started')
    
    rdconn.set("msg","hellow, redis")
    
    while True:
        try:
            msg = rdconn.get('msg')
            rdconn.delete('msg')
            
            logger.info(f'redis msg: {msg}')
            time.sleep(2)
        except KeyboardInterrupt:
            break 
        except Exception:
            logger.exception('redis error')
            break 
    logger.info('redis stoped')
    pass
