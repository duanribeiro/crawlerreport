import cProfile
import io
import pstats

def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)


def profile(fnc):
    """A decorator that uses cProfile to profile a function"""

    def inner(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()
        retval = fnc(*args, **kwargs)
        pr.disable()
        s = io.StringIO()
        sortby = 'cumulative'
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print(s.getvalue())
        with open('result_scrapy.txt', 'w+') as f:
            f.write(s.getvalue())

        return retval

    return inner
