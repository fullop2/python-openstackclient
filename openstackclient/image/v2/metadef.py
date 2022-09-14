#   Copyright 2012-2013 OpenStack Foundation
#
#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#

"""Image V2 Action Implementations"""

import argparse
from base64 import b64encode
import logging
import os
import sys
import json

from cinderclient import api_versions
from openstack.image import image_signer
from osc_lib.api import utils as api_utils
from osc_lib.cli import format_columns
from osc_lib.cli import parseractions
from osc_lib.command import command
from osc_lib import exceptions
from osc_lib import utils
from oslo_utils import uuidutils

from openstackclient.common import progressbar
from openstackclient.i18n import _
from openstackclient.identity import common

if os.name == "nt":
    import msvcrt
else:
    msvcrt = None


def _format_metadata_object(metadata_object, human_readable=False):
    """Format an image to make it more consistent with OSC operations."""

    info = {}
    properties = {}

    fields_to_show = [
        'name','namespace','properties'
    ]
    metadata_object = json.loads(metadata_object)

    for key in metadata_object:
        if key in fields_to_show:
            info[key] = metadata_object.get(key)

    if properties:
        info['properties'] = format_columns.DictColumn(properties)

    return info


class CreateMetadataObject(command.ShowOne):
    _description = _("Create metadata object")

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            "--name",
            metavar="<object-name>",
            help=_("New object name"),
        )
        parser.add_argument(
            "--namespace",
            metavar="<namespace>",
            help=_("namespace"),
        )
        parser.add_argument(
            "--properties",
            metavar="<properties>",
            help=_("Object schema JSON format"),
        )
        common.add_project_domain_option_to_parser(parser)

        return parser

    def take_action(self, parsed_args):
        image_client = self.app.client_manager.image

        kwargs = {'allow_duplicates': True}
        copy_attrs = ('name', 'namespace', 'properties')
        for attr in copy_attrs:
            if attr in parsed_args:
                val = getattr(parsed_args, attr, None)
                if val:
                    kwargs[attr] = val

        metadata_object = image_client.create_metadata_object(**kwargs)
        info = _format_metadata_object(metadata_object.text)
        return zip(*sorted(info.items()))


class DeleteMetadataObject(command.Command):
    _description = _("Create metadata object")

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            "--name",
            metavar="<object-name>",
            help=_("New object name"),
        )
        parser.add_argument(
            "--namespace",
            metavar="<namespace>",
            help=_("namespace"),
        )

        return parser

    def take_action(self, parsed_args):
        image_client = self.app.client_manager.image

        kwargs = {'allow_duplicates': True}
        copy_attrs = ('name', 'namespace')
        for attr in copy_attrs:
            if attr in parsed_args:
                val = getattr(parsed_args, attr, None)
                if val:
                    kwargs[attr] = val

        metadata_object = image_client.delete_metadata_object(**kwargs)


class GetMetadataObject(command.ShowOne):
    _description = _("Get metadata object")

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            "name",
            metavar="<object-name>",
            help=_("object name"),
        )
        parser.add_argument(
            "namespace",
            metavar="<namespace>",
            help=_("namespace"),
        )
        common.add_project_domain_option_to_parser(parser)

        return parser

    def take_action(self, parsed_args):
        image_client = self.app.client_manager.image

        kwargs = {'allow_duplicates': True}
        copy_attrs = ('name', 'namespace', 'properties')
        for attr in copy_attrs:
            if attr in parsed_args:
                val = getattr(parsed_args, attr, None)
                if val:
                    kwargs[attr] = val

        metadata_object = image_client.get_metadata_object(**kwargs)
        info = _format_metadata_object(metadata_object.text)
        return zip(*sorted(info.items()))
