import logging 


logger = logging.getLogger(__name__)


def test():
    logger.debug('debug')
    logger.info('info')
    logger.warning('warning')
    logger.error('error')
    logger.critical('critical') 
    

def divide_numbers(a, b):
    if b == 0:
        logger.error('b is zero')
        return 'error'
    else:
        return a / b
    
    

if __name__ == '__main__':
    test()
    print(divide_numbers(10, 0))