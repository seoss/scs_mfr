#!/usr/bin/env python3

"""
Created on 28 Dec 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

command line example:
./scs_mfr/gpi.py P9_12 -w 0 -v
"""

import sys
import time

from scs_comms.modem.at_command import ATCommand
from scs_comms.modem.ge910 import GE910

from scs_core.data.json import JSONify
from scs_core.sys.exception_report import ExceptionReport

from scs_mfr.cmd.cmd_ge910 import CmdGE910


# --------------------------------------------------------------------------------------------------------------------

class CommandSequencer(object):
    """
    classdocs
    """
    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, script_name):
        """
        Constructor
        """
        self.__script_name = script_name
        self.__file = sys.stdin if script_name is None else open(script_name)


    # ----------------------------------------------------------------------------------------------------------------

    def commands(self):
        text = ""

        while True:
            if self.__script_name is None:
                print("> ", end="")
                sys.stdout.flush()

                line = self.__file.readline()
                sys.stdout.flush()

                if len(line) > 1:
                    text = line.strip()

            else:
                line = self.__file.readline()

                if len(line) == 0:
                    self.__file.close()
                    return

                if len(line) == 1:
                    continue

                text = line.strip()

                print("> %s" % text)

            yield ATCommand.construct(text)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "CommandSequencer:{script_name:%s}" % self.__script_name



# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    cmd = None
    modem = None

    try:
        # ------------------------------------------------------------------------------------------------------------
        # cmd...

        cmd = CmdGE910()

        if cmd.verbose:
            print(cmd, file=sys.stderr)


        # ------------------------------------------------------------------------------------------------------------
        # resource...

        modem = GE910(True)
        modem.switch_on()

        if cmd.verbose:
            print(modem, file=sys.stderr)

        sequencer = CommandSequencer(cmd.script)


        # ------------------------------------------------------------------------------------------------------------
        # run...

        for command in sequencer.commands():
            start_time = time.time()
            response = modem.execute(command)
            print(response)
            print("time: %0.3f" % (time.time() - start_time))
            print("")


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except KeyboardInterrupt as ex:
        if cmd.verbose:
            print("ge910: KeyboardInterrupt", file=sys.stderr)

    except Exception as ex:
        print(JSONify.dumps(ExceptionReport.construct(ex)), file=sys.stderr)

    finally:
        if modem:
            modem.switch_off()
