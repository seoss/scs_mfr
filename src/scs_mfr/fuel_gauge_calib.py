#!/usr/bin/env python3

"""
Created on 4 Apr 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The fuel_gauge_calib utility is used to interrogate or update the fuel gauge parameters on an attached battery pack.

Parameters are found automatically though a learning process run by the fuel gauge throughout its lifetime. The battery
pack model incorporates a set of parameter values gained through this process, referred to as the default parameters.

When a new fuel gauge is put into use, it can be initialised with these values using the fuel_gauge_calib utility
--initialise flag - this sets both the parameters and the fuel gauge configuration.

SYNOPSIS
fuel_gauge_calib.py { -i | -d | -c | -f  | -p } [-v]

EXAMPLES
./fuel_gauge_calib.py -cv

DOCUMENT EXAMPLE - PARAMETERS
{"r-comp-0": 171, "temp-co": 8766, "full-cap-rep": 16712, "full-cap-nom": 41298, "cycles": 966}

DOCUMENT EXAMPLE - FUEL
{"chrg": {"%": 94.4, "mah": 7889}, "tte": 71156, "ttf": null, "curr": -278, "g-tmp": 22.8, "cap": 10818, "cyc": 0.0}

DOCUMENT EXAMPLE - PSU
{"standby": false, "pwr-in": 3.9, "batt": {"chg": 3, "tte": null, "ttf": 11801}}

SEE ALSO
scs_dev/psu_monitor
scs_mfr/psu_conf
"""

import sys

from scs_core.data.json import JSONify

from scs_dfe.interface.interface_conf import InterfaceConf

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_fuel_gauge_calib import CmdFuelGaugeCalib

from scs_psu.psu.psu_conf import PSUConf


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdFuelGaugeCalib()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    if cmd.verbose:
        print("fuel_gauge_calib: %s" % cmd, file=sys.stderr)
        sys.stderr.flush()

    try:
        I2C.open(Host.I2C_SENSORS)

        # ------------------------------------------------------------------------------------------------------------
        # resources...

        # Interface...
        interface_conf = InterfaceConf.load(Host)

        # PSU...
        psu_conf = PSUConf.load(Host)
        psu = psu_conf.psu(Host, interface_conf.model)

        if cmd.verbose:
            print("fuel_gauge_calib: %s" % psu, file=sys.stderr)

        batt_pack = psu.batt_pack

        if batt_pack is None:
            print("fuel_gauge_calib: PSU has no battery pack.", file=sys.stderr)
            exit(1)


        # ------------------------------------------------------------------------------------------------------------
        # run...

        # no auto-initialisation - we want to see the MAX17055 native values

        if cmd.initialise:
            batt_pack.initialise(force_config=True)

        elif cmd.default:
            params = batt_pack.default_params()
            print(JSONify.dumps(params))

        elif cmd.current:
            params = batt_pack.read_learned_params()
            print(JSONify.dumps(params))

        elif cmd.fuel:
            datum = batt_pack.sample()
            print(JSONify.dumps(datum))

        elif cmd.power:
            datum = psu.status()
            print(JSONify.dumps(datum))


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    finally:
        I2C.close()
