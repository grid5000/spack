# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import stat

import pytest

import llnl.util.filesystem as fs

from spack.util.file_permissions import InvalidPermissionsError, set_permissions


def test_chmod_real_entries_ignores_suid_sgid(tmpdir):
    path = str(tmpdir.join('file').ensure())
    mode = stat.S_ISUID | stat.S_ISGID | stat.S_ISVTX
    os.chmod(path, mode)
    mode = os.stat(path).st_mode  # adds a high bit we aren't concerned with

    perms = stat.S_IRWXU
    set_permissions(path, perms)

    assert os.stat(path).st_mode == mode | perms & ~stat.S_IXUSR


def test_chmod_rejects_group_writable_suid(tmpdir):
    path = str(tmpdir.join('file').ensure())
    mode = stat.S_ISUID
    fs.chmod_x(path, mode)

    perms = stat.S_IWGRP
    with pytest.raises(InvalidPermissionsError):
        set_permissions(path, perms)


def test_chmod_rejects_world_writable_suid(tmpdir):
    path = str(tmpdir.join('file').ensure())
    mode = stat.S_ISUID
    fs.chmod_x(path, mode)

    perms = stat.S_IWOTH
    with pytest.raises(InvalidPermissionsError):
        set_permissions(path, perms)


def test_chmod_rejects_world_writable_sgid(tmpdir):
    path = str(tmpdir.join('file').ensure())
    mode = stat.S_ISGID
    fs.chmod_x(path, mode)

    perms = stat.S_IWOTH
    with pytest.raises(InvalidPermissionsError):
        set_permissions(path, perms)
