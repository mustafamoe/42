"""Exercise Makefile storage migration without installing or downloading."""

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


MAKEFILE = Path(__file__).resolve().parents[1] / "submission/Makefile"


class StorageTests(unittest.TestCase):
    """Keep source files and cached assets safe during relocation."""

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        self.project = self.root / "project"
        self.storage = self.root / "goinfre space"
        self.project.mkdir()
        shutil.copy2(MAKEFILE, self.project / "Makefile")

    def make(self, storage=None):
        return subprocess.run(
            ["make", "storage", f"GOINFRE={self.storage if storage is None else storage}"],
            cwd=self.project, text=True, capture_output=True,
        )

    def test_moves_existing_data_and_is_repeatable(self):
        for relative in (".venv", "model", "data/output"):
            path = self.project / relative
            path.mkdir(parents=True)
            (path / "preserved").write_text(relative)
        for _ in range(2):
            result = self.make()
            self.assertEqual(result.returncode, 0, result.stderr)
        for relative in (".venv", "model", "data/output"):
            path = self.project / relative
            self.assertTrue(path.is_symlink())
            self.assertEqual(path.resolve(), self.storage / path.name)
            self.assertEqual((path / "preserved").read_text(), relative)

    def test_creates_missing_directories_and_recovers_cleared_storage(self):
        self.assertEqual(self.make().returncode, 0)
        shutil.rmtree(self.storage)
        result = self.make()
        self.assertEqual(result.returncode, 0, result.stderr)
        for relative in (".venv", "model", "data/output"):
            self.assertTrue((self.project / relative).is_dir())

    def test_conflict_fails_before_moving_any_project_directory(self):
        (self.project / ".venv").mkdir()
        (self.storage / "model").mkdir(parents=True)
        result = self.make()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Storage already exists", result.stderr)
        self.assertFalse((self.project / ".venv").is_symlink())
        self.assertFalse((self.storage / ".venv").exists())

    def test_unrelated_link_is_preserved_before_any_migration(self):
        (self.project / ".venv").mkdir()
        other = self.root / "other-model"
        other.mkdir()
        (self.project / "model").symlink_to(other)
        result = self.make()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual((self.project / "model").resolve(), other)
        self.assertFalse((self.project / ".venv").is_symlink())

    def test_empty_setting_leaves_local_layout(self):
        self.assertEqual(self.make("").returncode, 0)
        self.assertFalse((self.project / ".venv").exists())
        self.assertFalse(self.storage.exists())

    def test_relative_storage_is_rejected(self):
        result = self.make("relative")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("absolute path", result.stderr)

    def test_project_root_cannot_create_self_referencing_links(self):
        result = self.make(str(self.project))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("must differ from the project directory", result.stderr)
        self.assertFalse((self.project / ".venv").exists())

    def test_install_receives_external_cache_and_python_paths(self):
        executable = self.root / "uv"
        executable.write_text(
            '#!/bin/sh\nprintf "%s\\n" "$UV_CACHE_DIR" '
            '"$UV_PYTHON_INSTALL_DIR" "$HF_HOME" "$*" > uv-invocation\n'
        )
        executable.chmod(0o755)
        environment = dict(os.environ, PATH=f"{self.root}:{os.environ['PATH']}")
        result = subprocess.run(
            ["make", "install", f"GOINFRE={self.storage}"],
            cwd=self.project, env=environment, text=True, capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((self.project / "uv-invocation").read_text().splitlines(), [
            str(self.storage / "uv-cache"), str(self.storage / "python"),
            str(self.storage / "huggingface"), "sync",
        ])
