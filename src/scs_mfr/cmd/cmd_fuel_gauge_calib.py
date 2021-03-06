"""
Created on 4 Apr 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse


# --------------------------------------------------------------------------------------------------------------------

class CmdFuelGaugeCalib(object):
    """unix command line handler"""

    def __init__(self):
        """
        Constructor
        """
        self.__parser = optparse.OptionParser(usage="%prog { -i | -c | -d | -l | -s | -f | -p } [-v]",
                                              version="%prog 1.0")

        # compulsory...
        self.__parser.add_option("--initialise", "-i", action="store_true", dest="initialise", default=False,
                                 help="initialise the fuel gauge configuration")

        self.__parser.add_option("--current", "-c", action="store_true", dest="current", default=False,
                                 help="report the current fuel gauge parameters")

        self.__parser.add_option("--default", "-d", action="store_true", dest="default", default=False,
                                 help="load default fuel gauge parameters")

        self.__parser.add_option("--load", "-l", action="store_true", dest="load", default=False,
                                 help="load fuel gauge parameters from filesystem")

        self.__parser.add_option("--save", "-s", action="store_true", dest="save", default=False,
                                 help="save the current fuel gauge parameters to filesystem")

        self.__parser.add_option("--fuel", "-f", action="store_true", dest="fuel", default=False,
                                 help="sample the fuel gauge")

        self.__parser.add_option("--power", "-p", action="store_true", dest="power", default=False,
                                 help="sample the PSU")

        # optional...
        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        count = 0

        if self.initialise:
            count += 1

        if self.default:
            count += 1

        if self.current:
            count += 1

        if self.save:
            count += 1

        if self.load:
            count += 1

        if self.fuel:
            count += 1

        if self.power:
            count += 1

        return count == 1


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def initialise(self):
        return self.__opts.initialise


    @property
    def default(self):
        return self.__opts.default


    @property
    def current(self):
        return self.__opts.current


    @property
    def save(self):
        return self.__opts.save


    @property
    def load(self):
        return self.__opts.load


    @property
    def fuel(self):
        return self.__opts.fuel


    @property
    def power(self):
        return self.__opts.power


    @property
    def verbose(self):
        return self.__opts.verbose


    # ----------------------------------------------------------------------------------------------------------------

    def print_help(self, file):
        self.__parser.print_help(file)


    def __str__(self, *args, **kwargs):
        return "CmdFuelGaugeCalib:{initialise:%s, default:%s, current:%s, save:%s, load:%s, " \
               "fuel:%s, power:%s, verbose:%s}" % \
               (self.initialise, self.default, self.current, self.save, self.load,
                self.fuel, self.power, self.verbose)
