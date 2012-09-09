'''This module contains classes used by pool core to interact with the rest of the pool.
   Default implementation do almost nothing, you probably want to override these classes
   and customize references to interface instances in your launcher.
   (see launcher_demo.tac for an example).
''' 

import time

import stratum.logger
log = stratum.logger.get_logger('interfaces')

class WorkerManagerInterface(object):
    def authorize(self, worker_name, worker_password):
        return True

class ShareManagerInterface(object):
    def on_submit_share(self, worker_name, block_header, block_hash, shares, timestamp, is_valid):
        log.info("%s %s %s" % ('Valid' if is_valid else 'INVALID', worker_name, block_hash))
    
    def on_submit_block(self, worker_name, block_header, block_hash, timestamp, is_accepted):
        log.info("Block %s %s" % (block_hash, 'ACCEPTED' if is_accepted else 'REJECTED'))
    
class TimestamperInterface(object):
    '''This is the only source for current time in the application.
    Override this for generating unix timestamp in different way.'''
    def time(self):
        return time.time()

class PredictableTimestamperInterface(TimestamperInterface):
    '''Predictable timestamper may be useful for unit testing.'''
    start_time = 1345678900 # Some day in year 2012
    delta = 0
    
    def time(self):
        self.delta += 1
        return self.start_time + self.delta
        
class Interfaces(object):
    worker_manager = None
    share_manager = None
    timestamper = None
    template_registry = None
    
    @classmethod
    def set_worker_manager(cls, manager):
        cls.worker_manager = manager    
    
    @classmethod        
    def set_share_manager(cls, manager):
        cls.share_manager = manager
    
    @classmethod
    def set_timestamper(cls, manager):
        cls.timestamper = manager
        
    @classmethod
    def set_template_registry(cls, registry):
        cls.template_registry = registry