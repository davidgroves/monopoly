''' Class to keep a log of the game
'''

import multiprocessing

class Log:
    ''' Class to handle logging of game events
    '''

    # Lock is declare on the class level,
    # so it would be shared among processes
    lock = multiprocessing.Lock()

    def __init__(self, log_file_name="log.txt", disabled=False):
        self.log_file_name = log_file_name
        self.content = []
        self.disabled = disabled

    def add(self, data):
        ''' Add a line to a Log
        '''
        if self.disabled:
            return
        self.content.append(data)

    def save(self):
        ''' Write out the log
        '''
        if self.disabled:
            return
        with self.lock:
            with open(self.log_file_name, "a", encoding="utf-8") as logfile:
                logfile.write("\n".join(self.content))
                if self.content:
                    logfile.write("\n")

    def reset(self):
        ''' Empty the log file
        '''
        with open(self.log_file_name, "w", encoding="utf-8") as _:
            pass
