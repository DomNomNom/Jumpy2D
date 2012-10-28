import time    
from contextlib import contextmanager

'''
To use this just do this:

with measureTime():
  myComplexFunction()
  
see http://stackoverflow.com/questions/2327719/timing-block-of-code-in-python-without-putting-it-in-a-function
'''

@contextmanager  
def measureTime(title=None):
    t1 = time.clock()
    yield
    t2 = time.clock()

    if title:
      print 'time taken for %s: %0.3f' % (repr(title), t2-t1)
    else:
      print 'time taken: %0.3f' % (t2-t1)

