# -*- Mode:Python; indent-tabs-mode:nil; tab-width:4 -*-
#
# Copyright 2022 Canonical Ltd.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import argparse
import sys
from unittest.mock import call

import craft_store.errors

from snapcraft import cli


def test_no_keyring_error(capsys, mocker):
    mocker.patch.object(sys, "argv", ["cmd", "whoami"])
    mock_version_cmd = mocker.patch(
        "snapcraft.commands.account.StoreWhoAmICommand.run",
        side_effect=craft_store.errors.NoKeyringError,
    )

    cli.run()

    assert mock_version_cmd.mock_calls == [call(argparse.Namespace())]
    stderr = capsys.readouterr().err.splitlines()

    # Simple verification that our expected message is being printed
    assert stderr[0].startswith(
        "craft-store error: No keyring found to store or retrieve credentials"
    )
    assert stderr[1].startswith(
        "Recommended resolution: Ensure the keyring is working or SNAPCRAFT_STORE_CREDENTIALS "
    )
    assert stderr[2].startswith(
        "For more information, check out: https://snapcraft.io/docs/snapcraft-authentication"
    )
