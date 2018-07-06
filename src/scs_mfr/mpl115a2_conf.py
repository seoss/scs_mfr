#!/usr/bin/env python3

"""
Created on 21 Jun 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The mpl115a2_conf utility is used to specify the altitude of the device hosting the MPL115A2 digital barometer. This
information is used to determine the pressure at sea level ("p0"). If the altitude is not specified, then
no p0 value is returned by the pressure_sampler utility.

Note that determination of p0 requires the temperature sensor in the MPL115A2 digital barometer to be calibrated. This
is done using the mpl115a2_calib utility.

Forthcoming versions of the mpl115a2_conf utility will support an "auto" mode, in which altitude is found from a GPS
receiver.

The pressure_sampler sampler processes must be restarted for changes to take effect.

SYNOPSIS
mpl115a2_conf.py [{ -a ALTITUDE | -d }] [-v]

EXAMPLES
./mpl115a2_conf.py -a 100

FILES
~/SCS/conf/mpl115a2_conf.json

DOCUMENT EXAMPLE
{"altitude": 100}

SEE ALSO
scs_dev/pressure_sampler
scs_mfr/mpl115a2_calib
"""

import sys

from scs_core.data.json import JSONify

from scs_dfe.climate.mpl115a2_conf import MPL115A2Conf

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_mpl115a2_conf import CmdMPL115A2Conf


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdMPL115A2Conf()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    if cmd.verbose:
        print("mpl115a2_conf: %s" % cmd, file=sys.stderr)
        sys.stderr.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    # DFEConf...
    conf = MPL115A2Conf.load(Host)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if cmd.set():
        conf = MPL115A2Conf(cmd.altitude)
        conf.save(Host)

    elif cmd.delete and conf is not None:
        conf.delete(Host)
        conf = None

    if conf:
        print(JSONify.dumps(conf))
