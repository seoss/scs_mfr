"""
Created on 09 Oct 2020

@author: Jade Page (jade.page@southcoastscience.com)
"""

import optparse


# --------------------------------------------------------------------------------------------------------------------

class CmdAWSSetup(object):
    """unix command line handler"""

    def __init__(self):
        """
        Constructor
        """
        self.__parser = optparse.OptionParser(usage="%prog [-g GROUP_NAME] [-c CORE_NAME] [-v] ", version="%prog 1.0")
        # optional...
        self.__parser.add_option("--group-name", "-g", action="store", dest="group_name", default=False,
                                 help="the name of the group to create")

        self.__parser.add_option("--core-name", "-c", action="store", dest="core_name", default=False,
                                 help="the name of the core to create")

        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()

    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if not bool(self.group_name) or not bool(self.core_name):
            return False
        return True

    # ----------------------------------------------------------------------------------------------------------------

    @property
    def group_name(self):
        return self.__opts.group_name

    @property
    def core_name(self):
        return self.__opts.core_name

    @property
    def verbose(self):
        return self.__opts.verbose

    # ----------------------------------------------------------------------------------------------------------------

    def print_help(self, file):
        self.__parser.print_help(file)

    def __str__(self, *args, **kwargs):
        return "CmdAWSSetup:{group-name:%s, core-name:%s, verbose:%s}" % (self.group_name, self.core_name, self.verbose)
