"""
Created on 13 Jul 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse

from scs_dfe.particulate.opc_conf import OPCConf

try:
    from scs_exegesis.particulate.exegete_catalogue import ExegeteCatalogue
except ImportError:
    from scs_core.exegesis.particulate.exegete_catalogue import ExegeteCatalogue


# --------------------------------------------------------------------------------------------------------------------

class CmdOPCConf(object):
    """
    unix command line handler
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        exegete_names = ExegeteCatalogue.model_names()
        exegetes = ' | '.join(exegete_names) if exegete_names else "none available"

        self.__parser = optparse.OptionParser(usage="%prog [-n NAME] [{ [-m MODEL] [-s SAMPLE_PERIOD] [-z { 0 | 1 }] "
                                                    "[-p { 0 | 1 }] [-b BUS] [-a ADDRESS] [-i INFERENCE_UDS] "
                                                    "[-e EXEGETE] [-r EXEGETE] | -d }] [-v]",
                                              version="%prog 1.0")

        # optional...
        self.__parser.add_option("--name", "-n", type="string", nargs=1, action="store", dest="name",
                                 help="the name of the OPC configuration")

        self.__parser.add_option("--model", "-m", type="string", nargs=1, action="store", dest="model",
                                 help="set MODEL { N2 | N3 | R1 | S30 }")

        self.__parser.add_option("--sample-period", "-s", type="int", nargs=1, action="store", dest="sample_period",
                                 help="set SAMPLE_PERIOD")

        self.__parser.add_option("--restart-on-zeroes", "-z", type="int", nargs=1, dest="restart_on_zeroes",
                                 action="store", help="restart on zero readings (default 1)")

        self.__parser.add_option("--power-saving", "-p", type="int", nargs=1, action="store", dest="power_saving",
                                 help="enable power saving mode (default 0)")

        self.__parser.add_option("--bus", "-b", type="int", nargs=1, action="store", dest="bus",
                                 help="override default host bus")

        self.__parser.add_option("--address", "-a", type="int", nargs=1, action="store", dest="address",
                                 help="override default host chip select or address")

        self.__parser.add_option("--inference", "-i", type="string", nargs=1, action="store", dest="inference",
                                 help="set inference server UDS")

        self.__parser.add_option("--exegete", "-e", type="string", nargs=1, action="store", dest="use_exegete",
                                 help="use EXEGETE { %s }" % exegetes)

        self.__parser.add_option("--remove-exegete", "-r", type="string", nargs=1, action="store",
                                 dest="remove_exegete", help="remove named EXEGETE")

        self.__parser.add_option("--delete", "-d", action="store_true", dest="delete", default=False,
                                 help="delete the OPC configuration")

        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.set() and self.delete:
            return False

        if self.model and not OPCConf.is_valid_model(self.model):
            return False

        if self.__opts.restart_on_zeroes is not None and \
                not (self.__opts.restart_on_zeroes == 0 or self.__opts.restart_on_zeroes == 1):
            return False

        if self.__opts.power_saving is not None and \
                not (self.__opts.power_saving == 0 or self.__opts.power_saving == 1):
            return False

        if self.use_exegete is not None and self.use_exegete not in ExegeteCatalogue.model_names():
            return False

        return True


    def is_complete(self):
        if self.model is None or self.sample_period is None or \
                self.restart_on_zeroes is None or self.power_saving is None:
            return False

        return True


    def set(self):
        return self.model is not None or self.sample_period is not None or \
               self.restart_on_zeroes is not None or self.power_saving is not None \
               or self.bus is not None or self.address is not None \
               or self.inference is not None or self.use_exegete is not None or self.remove_exegete is not None


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def name(self):
        return self.__opts.name


    @property
    def model(self):
        return self.__opts.model


    @property
    def sample_period(self):
        return self.__opts.sample_period


    @property
    def restart_on_zeroes(self):
        return None if self.__opts.restart_on_zeroes is None else bool(self.__opts.restart_on_zeroes)


    @property
    def power_saving(self):
        return None if self.__opts.power_saving is None else bool(self.__opts.power_saving)


    @property
    def bus(self):
        return self.__opts.bus


    @property
    def address(self):
        return self.__opts.address


    @property
    def use_exegete(self):
        return self.__opts.use_exegete


    @property
    def inference(self):
        return self.__opts.inference


    @property
    def remove_exegete(self):
        return self.__opts.remove_exegete


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
        return "CmdOPCConf:{name:%s, model:%s, sample_period:%s, restart_on_zeroes:%s, power_saving:%s, " \
               "bus:%s, address:%s, inference:%s, use_exegete:%s, remove_exegete:%s, " \
               "delete:%s, verbose:%s}" % \
               (self.name, self.model, self.sample_period, self.restart_on_zeroes, self.power_saving,
                self.bus, self.address, self.inference, self.use_exegete, self.remove_exegete,
                self.delete, self.verbose)
