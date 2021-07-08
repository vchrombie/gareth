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


"""Tool to manage the developer installation of GrimoireLab."""

import os
import subprocess

import click
import git.repo.base as grb

from github import Github, BadCredentialsException, GithubException

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

GITHUB_URL = "https://github.com/"

CHECKOUT_MASTER_CMD = ['git', 'checkout', 'master']
FETCH_UPSTREAM_CMD = ['git', 'fetch', 'upstream']
REBASE_UPSTREAM_CMD = ['git', 'rebase', 'upstream/master']


def source_prompt():
    """Prompt source to read the folder name"""
    prompt_msg = ">> Please provide the source folder name"
    return prompt_msg


def validate_source(ctx, value):
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
    """Tool to manage the developer installation of GrimoireLab."""
    if operation == 'create' and not token:
        msg = "Token is required for creating the dev setup.\n"
        msg += "Please provide the token using the '-t'/'--token' flag."
        raise click.ClickException(msg)

    if operation == 'create':
        create_dev_setup(token, source)
    elif operation == 'update':
        update_dev_setup(source)


def validate_token(token):
    """Check and validate the GitHub API Token."""
    g = Github(token)
    try:
        user = g.get_user()
        click.echo("Access token is working, {}.\n".format(user.login))
        return g
    except BadCredentialsException as ex:
        msg = "Invalid token.\n"
        msg += str(ex)
        raise click.ClickException(msg)
    except Exception as ex:
        raise click.ClickException(ex)


def change_the_directory(dirpath):
    """Change the directory"""
    try:
        os.chdir(dirpath)
    except Exception as ex:
        raise click.ClickException(ex)


def fork_the_repository(user, repo):
    """Fork the respository"""
    try:
        user.create_fork(repo)
    except GithubException as ex:
        msg = "Forking aborted.\n"
        msg += "Please select the appropriate scope (`repo`) for the token.\n"
        msg += str(ex)
        raise click.ClickException(msg)


def clone_the_repository(user, repo):
    """Clone the forked repository"""
    try:
        return grb.Repo.clone_from(
            GITHUB_URL + user.login + "/" + repo.name + ".git",
            "{0}/{1}".format(os.getcwd(), repo.name)
        )
    except grb.GitCommandError as ex:
        raise click.ClickException(ex)


def set_upstream(local_repo_path, org, repo):
    """Set upstream to the forked repository"""
    try:
        grb.Repo.create_remote(
            local_repo_path, "upstream",
            GITHUB_URL + org.login + "/" + repo.name + ".git"
        )
    except grb.GitCommandError as ex:
        msg = str(ex)
        click.ClickException(msg)


def sync_with_upstream():
    """Rebase the fork with upstream"""
    subprocess.call(CHECKOUT_MASTER_CMD)
    subprocess.call(FETCH_UPSTREAM_CMD)
    subprocess.call(REBASE_UPSTREAM_CMD)


def create_dev_setup(token, source):
    """Create the developer setup"""
    g = validate_token(token)

    click.echo("Creating the developer setup.\n")

    user = g.get_user()

    source_path = os.path.join(os.getcwd(), source)

    for repository in REPOS:
        click.echo("{}...".format(repository), nl=False)

        change_the_directory(source_path)

        org, repo = repository.split('/')
        org = g.get_organization(org)
        repo = org.get_repo(repo)

        fork_the_repository(user, repo)
        local_repo_path = clone_the_repository(user, repo)
        set_upstream(local_repo_path, org, repo)

        click.echo("done")

    click.echo()
    click.echo("The dev setup is created.")


def update_dev_setup(source):
    """Update the developer setup"""
    click.echo("Updating the developer setup.\n")

    source_path = os.path.join(os.getcwd(), source)

    for repository in REPOS:
        click.echo("{}...".format(repository))

        repo = repository.split('/')[-1]
        dirpath = os.path.join(source_path, repo)

        change_the_directory(dirpath)

        sync_with_upstream()

        click.echo("done\n")

    click.echo()
    click.echo("The dev setup is updated.")


if __name__ == '__main__':
    main()
