#!/usr/bin/env python3

"""
Created on 18 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

workflow:
  1: ./system_id.py
  2: ./api_auth.py
  3: ./host_device.py
> 4: ./host_project.py

Requires APIAuth, SystemID and AFECalib documents.
Creates Project document.

Warning: schema IDs are not updated when an existing topic is updated - create a new topic instead. 

command line example:
./host_project.py -v -s field-trial 2
"""

import sys

from scs_core.data.json import JSONify
from scs_core.osio.client.api_auth import APIAuth
from scs_core.osio.config.project import Project
from scs_core.osio.config.project_schema import ProjectSchema
from scs_core.osio.data.topic import Topic
from scs_core.osio.data.topic_info import TopicInfo
from scs_core.osio.manager.topic_manager import TopicManager
from scs_core.sys.system_id import SystemID

from scs_dfe.gas.afe_calib import AFECalib

from scs_host.client.http_client import HTTPClient
from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_host_project import CmdHostProject


# --------------------------------------------------------------------------------------------------------------------

class HostProject(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, topic_manager):
        """
        Constructor
        """
        self.__topic_manager = topic_manager


    # ----------------------------------------------------------------------------------------------------------------

    def construct_topic(self, path, schema):
        topic = self.__topic_manager.find(path)

        if topic:
            updated = Topic(None, schema.name, schema.description, topic.is_public, topic.info, None, None)

            self.__topic_manager.update(topic.path, updated)

        else:
            info = TopicInfo(TopicInfo.FORMAT_JSON, None, None, None)     # for the v2 API, schema_id goes in Topic
            constructed = Topic(path, schema.name, schema.description, True, True, info, schema.schema_id)

            self.__topic_manager.create(constructed)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "HostProject:{topic_manager:%s}" % self.__topic_manager


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdHostProject()

    if cmd.verbose:
        print(cmd, file=sys.stderr)


    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    # APIAuth...
    api_auth = APIAuth.load_from_host(Host)

    if api_auth is None:
        print("APIAuth not available.", file=sys.stderr)
        exit()

    if cmd.verbose:
        print(api_auth, file=sys.stderr)


    # SystemID...
    system_id = SystemID.load_from_host(Host)

    if system_id is None:
        print("SystemID not available.", file=sys.stderr)
        exit()

    if cmd.verbose:
        print(system_id, file=sys.stderr)


    # AFECalib...
    afe_calib = AFECalib.load_from_host(Host)

    if afe_calib is None:
        print("AFECalib not available.", file=sys.stderr)
        exit()

    if cmd.verbose:
        print(afe_calib, file=sys.stderr)


    # manager...
    manager = TopicManager(HTTPClient(), api_auth.api_key)

    creator = HostProject(manager)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if cmd.set():
        project = Project.construct(api_auth.org_id, cmd.group, cmd.location_id)

        gases_schema = ProjectSchema.find_gas_schema(afe_calib.gas_names())

        creator.construct_topic(project.climate_topic_path(), ProjectSchema.CLIMATE)
        creator.construct_topic(project.gases_topic_path(), gases_schema)

        if cmd.particulates:
            creator.construct_topic(project.particulates_topic_path(), ProjectSchema.PARTICULATES)

        creator.construct_topic(project.status_topic_path(system_id), ProjectSchema.STATUS)
        creator.construct_topic(project.control_topic_path(system_id), ProjectSchema.CONTROL)

        project.save(Host)

    project = Project.load_from_host(Host)
    print(JSONify.dumps(project))

    if cmd.verbose:
        print("-", file=sys.stderr)

        found = manager.find(project.climate_topic_path())

        if found is not None:
            print("climate_topic:      %s" % found.path, file=sys.stderr)

        found = manager.find(project.gases_topic_path())

        if found is not None:
            print("gases_topic:        %s" % found.path, file=sys.stderr)

        found = manager.find(project.particulates_topic_path())

        if found is not None:
            print("particulates_topic: %s" % found.path, file=sys.stderr)

        found = manager.find(project.status_topic_path(system_id))

        if found is not None:
            print("status_topic:       %s" % found.path, file=sys.stderr)

        found = manager.find(project.control_topic_path(system_id))

        if found is not None:
            print("control_topic:      %s" % found.path, file=sys.stderr)
