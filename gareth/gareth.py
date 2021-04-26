#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 2015-2021 Bitergia
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# Authors:
#     Venu Vardhan Reddy Tekula <venu@bitergia.com>
#


"""
Tool to manage the developer installation of GrimoireLab.
"""

import os

import click

REPOS = [
    "chaoss/grimoirelab-sirmordred",
    "chaoss/grimoirelab-toolkit",
    "chaoss/grimoirelab-perceval",
    "chaoss/grimoirelab-perceval-mozilla",
    "chaoss/grimoirelab-perceval-opnfv",
    "chaoss/grimoirelab-perceval-puppet",
    "chaoss/grimoirelab-perceval-weblate",
    "Bitergia/grimoirelab-perceval-finos",
    "chaoss/grimoirelab-graal",
    "chaoss/grimoirelab-elk",
    "chaoss/grimoirelab-sortinghat",
    "chaoss/grimoirelab-sigils",
    "chaoss/grimoirelab-kidash",
    "chaoss/grimoirelab-cereslib",
    "chaoss/grimoirelab-kingarthur",
    "chaoss/grimoirelab-manuscripts"
]


def source_prompt():
    """Prompt source to read the folder name"""

    prompt_msg = ">> Please provide the source folder name"
    return prompt_msg


def validate_source(ctx, param, value):
    """Check source option"""

    click.echo()

    if os.path.exists(value):
        return value

    click.echo("Error: {} directory does not exist".format(value))

    if not click.confirm("Do you want to create it?"):
        msg = "The deveoper setup needs a source directory.\n"
        raise click.ClickException(msg)

    try:
        os.mkdir(value)
        click.echo("The '{}' directory is created.\n".format(value))
    except OSError as ex:
        msg = "Unable to create directory.\n"
        msg += str(ex)
        raise click.ClickException(msg)

    return value


@click.command()
@click.option('-t', '--token', required=False,
              help="GitHub API Token.")
@click.option('-s', '--source',
              prompt=source_prompt(),
              default="sources", show_default=True,
              callback=validate_source,
              help="The source folder of the dev env.")
@click.option('--create', 'operation', flag_value='create',
              default=True,
              help="Create the developer setup.")
@click.option('--update', 'operation', flag_value='update',
              help="Update the developer setup.")
def main(token, source, operation):
    """
    Tool to manage the developer installation of GrimoireLab.
    """

    if operation == 'create':
        create_dev_setup(token, source)
    elif operation == 'update':
        update_dev_setup(source)


if __name__ == '__main__':
    main()
