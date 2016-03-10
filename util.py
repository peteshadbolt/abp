""" 
Provides a decorator to cache function output to disk
"""
import cPickle

def cache_to_disk(file_name):
    def wrap(func):
        def modified(*args, **kwargs):
            try:
                output = cPickle.load(open(file_name, "r"))
            except (IOError, ValueError):
                output = func(*args, **kwargs)
                with open(file_name, "w") as f:
                    cPickle.dump(output, f)
            return output
        return modified
    return wrap
