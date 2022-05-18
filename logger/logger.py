

'''
class Log performs logger configuration, creeation, multiprocess listener.
create by AlinKwon
'''


import logging
from logging.handlers import TimedRotatingFileHandler
import os
from threading import Thread


class Log():
    def __init__(self):
        self.th = None
        self.logger = logging.getLogger('mp')
        if not os.path.exists("./logs/"):
            os.makedirs("./logs/")
        log_file_handler = TimedRotatingFileHandler(filename="./logs/selfstore.log", when="midnight", interval=1, backupCount=15, encoding='UTF-8')
        log_file_handler.setFormatter(logging.Formatter('%(asctime)s\tFile \"%(filename)s\",line %(lineno)s\t%(levelname)s: %(message)s')) 
        self.logger.addHandler(log_file_handler)
        self.logger.addHandler(logging.StreamHandler())
        self.logger.setLevel(level=logging.DEBUG)
    
    def listenerStart(self, queue):
        if self.th != None:
            self.logger.error("Error Create Logging Thread!!!!!")
            raise Exception("Log already started")
        self.logger.info('Logging start =================================================================')
        self.th = Thread(target=self._procLogQueue,args = (queue,))
        self.th.start()

    def listenerStop(self,queue):
        if self.th == None:
            self.logger.error("Listener stopped")
            raise Exception("Listener stopped")
        queue.put(None)
        self.th.join()
        self.logger.info('Logging End   =================================================================')
    
    @staticmethod
    def getQueueLogger(queue, name):
        qh = logging.handlers.QueueHandler(queue=queue)
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(qh)
        return logger

    def _procLogQueue(self,queue):
        self.logger.info('log queue start----------------------------------------------------------------')
        while True:
            try:
                record = queue.get()
                if record is None:
                    break 
                self.logger.handle(record)
            except Exception:
                self.logger.error('logger queue error')
        self.logger.info('log queue end  ----------------------------------------------------------------')



def testWorker(queue):
    LEVELS = [logging.DEBUG, logging.INFO, logging.WARNING,
            logging.ERROR, logging.CRITICAL]
    MESSAGES = ['Random message #1', 
            'Random message #2',
            'Random message #3',
            ]
    from random import choice, random
    import time

    logger = Log.getQueueLogger(queue, 'test')
    name = multiprocessing.current_process().name
    for i in range(5):
        time.sleep(random())
        level = choice(LEVELS)
        message = choice(MESSAGES)
        logger.log(level, f'{name} - {message}')

    logger.info(f'{name} finished')   

if __name__ == '__main__':
    import multiprocessing
   
    queue = multiprocessing.Queue(-1)

    listener = Log()
    listener.listenerStart(queue)  # log consumer thread start

    workers = []
    for i in range(3):  # multiprocess loop
        w = multiprocessing.Process(target=testWorker, args=(queue,))
        workers.append(w)

    [p.start() for p in workers]        
    [p.join()  for p in workers]
    
    listener.listenerStop(queue)  # log consumer thread end
    pass