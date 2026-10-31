"""Pruebas de utilidades compartidas del pipeline."""
import os
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from knee.common import resolve_data_dir


class ResolveDataDirTests(unittest.TestCase):
    def test_returns_directory_with_both_required_files(self):
        with tempfile.TemporaryDirectory() as path:
            for name in ("train.csv", "train_series.csv"):
                open(os.path.join(path, name), "w").close()

            self.assertEqual(resolve_data_dir(path), path)

    def test_rejects_directory_missing_train_csv(self):
        with tempfile.TemporaryDirectory() as path:
            open(os.path.join(path, "train_series.csv"), "w").close()
            with patch("knee.common.os.walk", return_value=[]):
                with self.assertRaises(FileNotFoundError):
                    resolve_data_dir(path)

    def test_finds_complete_dataset_under_kaggle_input(self):
        with tempfile.TemporaryDirectory() as path:
            with patch(
                "knee.common.os.walk",
                return_value=[(path, [], ["train.csv", "train_series.csv"])],
            ):
                self.assertEqual(resolve_data_dir("missing"), path)


if __name__ == "__main__":
    unittest.main()
