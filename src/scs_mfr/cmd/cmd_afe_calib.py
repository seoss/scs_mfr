"""
Created on 27 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse

from datetime import date


# --------------------------------------------------------------------------------------------------------------------

class CmdAFECalib(object):
    """unix command line handler"""

    def __init__(self):
        """
        Constructor
        """
        self.__parser = optparse.OptionParser(usage="%prog [{ -a SERIAL_NUMBER | -s SERIAL_NUMBER YYYY-MM-DD | -t  | "
                                                    "-d }] [-v]", version="%prog 1.0")

        # optional...
        self.__parser.add_option("--afe", "-a", type="string", nargs=1, action="store", dest="afe_serial_number",
                                 help="set AFE serial number")

        self.__parser.add_option("--sensor", "-s", type="string", nargs=2, action="store", dest="sensor",
                                 help="set single sensor serial number and calibration date")

        self.__parser.add_option("--test", "-t", action="store_true", dest="test", default=False,
                                 help="set AFE as test load")

        self.__parser.add_option("--delete", "-d", action="store_true", dest="delete", default=False,
                                 help="delete this calibration")

        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        count = 0

        if self.afe_serial_number is not None:
            count += 1

        if self.sensor is not None:
            count += 1

        if self.test:
            count += 1

        if self.delete:
            count += 1

        if count > 1:
            return False

        return True


    # ----------------------------------------------------------------------------------------------------------------

    def set(self):
        return self.afe_serial_number is not None or self.sensor is not None or self.test


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def afe_serial_number(self):
        return self.__opts.afe_serial_number


    @property
    def sensor(self):
        return self.__opts.sensor


    @property
    def sensor_serial_number(self):
        return None if self.__opts.sensor is None else self.__opts.sensor[0]


    @property
    def sensor_calibration_date_str(self):
        return None if self.__opts.sensor is None else self.__opts.sensor[1]


    @property
    def sensor_calibration_date(self):
        if self.__opts.sensor is None:
            return None

        pieces = self.__opts.sensor[1].split('-')
        return date(int(pieces[0]), int(pieces[1]), int(pieces[2]))


    @property
    def test(self):
        return self.__opts.test


    @property
    def delete(self):
        return self.__opts.delete


    @property
    def verbose(self):
        return self.__opts.verbose


    # ----------------------------------------------------------------------------------------------------------------

    def print_help(self, file):
        self.__parser.print_help(file)


    def __str__(self, *args, **kwargs):
        return "CmdAFECalib:{afe_serial_number:%s, sensor:%s, test:%s, delete:%s, verbose:%s}" % \
               (self.afe_serial_number, self.sensor, self.test, self.delete, self.verbose)
