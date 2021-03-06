"""
Created on 13 Jul 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse


# --------------------------------------------------------------------------------------------------------------------

class CmdSampler(object):
    """unix command line handler"""

    def __init__(self):
        """
        Constructor
        """
        self.__parser = optparse.OptionParser(usage="%prog { -s SEMAPHORE | -i INTERVAL [-n SAMPLES]} [-v]",
                                              version="%prog 1.0")

        # optional...
        self.__parser.add_option("--semaphore", "-s", type="string", nargs=1, action="store", dest="semaphore",
                                 help="sampling controlled by SEMAPHORE")

        self.__parser.add_option("--interval", "-i", type="float", nargs=1, action="store", dest="interval",
                                 help="sampling interval in seconds")

        self.__parser.add_option("--samples", "-n", type="int", nargs=1, action="store", dest="samples",
                                 help="number of samples (default for-ever)")

        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if bool(self.semaphore is None) == bool(self.interval is None):
            return False

        if self.interval is None and self.samples is not None:
            return False

        return True


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def semaphore(self):
        return self.__opts.semaphore


    @property
    def interval(self):
        return self.__opts.interval


    @property
    def samples(self):
        return self.__opts.samples


    @property
    def verbose(self):
        return self.__opts.verbose


    # ----------------------------------------------------------------------------------------------------------------

    def print_help(self, file):
        self.__parser.print_help(file)


    def __str__(self, *args, **kwargs):
        return "CmdSampler:{semaphore:%s, interval:%s, samples:%s, verbose:%s}" % \
                    (self.semaphore, self.interval, self.samples, self.verbose)
