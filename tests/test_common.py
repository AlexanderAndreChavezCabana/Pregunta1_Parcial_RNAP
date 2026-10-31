"""Pruebas de utilidades compartidas del pipeline."""
import os
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from knee.common import find_file, resolve_data_dir


class ResolveDataDirTests(unittest.TestCase):
    def test_returns_directory_with_both_required_files(self):
        with tempfile.TemporaryDirectory() as path:
            for name in ("train.csv", "train_series.csv"):
                open(os.path.join(path, name), "w").close()
            os.mkdir(os.path.join(path, "train_series"))

            self.assertEqual(resolve_data_dir(path), path)

    def test_rejects_directory_missing_dicom_series(self):
        with tempfile.TemporaryDirectory() as path:
            for name in ("train.csv", "train_series.csv"):
                open(os.path.join(path, name), "w").close()
            with patch("knee.common.os.walk", return_value=[]):
                with self.assertRaises(FileNotFoundError):
                    resolve_data_dir(path)

    def test_rejects_directory_missing_train_csv(self):
        with tempfile.TemporaryDirectory() as path:
            open(os.path.join(path, "train_series.csv"), "w").close()
            with patch("knee.common.os.walk", return_value=[]):
                with self.assertRaises(FileNotFoundError):
                    resolve_data_dir(path)

    def test_finds_complete_dataset_under_kaggle_input(self):
        with tempfile.TemporaryDirectory() as path:
            os.mkdir(os.path.join(path, "train_series"))
            with patch(
                "knee.common.os.walk",
                return_value=[(path, ["train_series"], ["train.csv", "train_series.csv"])],
            ):
                self.assertEqual(resolve_data_dir("missing"), path)


class FindFileTests(unittest.TestCase):
    def test_returns_existing_local_file(self):
        with tempfile.TemporaryDirectory() as path:
            local_file = os.path.join(path, "result.csv")
            open(local_file, "w").close()

            self.assertEqual(find_file("result.csv", local_file), local_file)

    def test_finds_file_under_search_root(self):
        with tempfile.TemporaryDirectory() as path:
            found_file = os.path.join(path, "result.csv")
            with patch(
                "knee.common.os.walk",
                return_value=[(path, [], ["result.csv"])],
            ):
                self.assertEqual(find_file("result.csv", "missing", path), found_file)

    def test_does_not_accept_directory_as_local_file(self):
        with tempfile.TemporaryDirectory() as path:
            local_dir = os.path.join(path, "result.csv")
            os.mkdir(local_dir)
            with patch("knee.common.os.walk", return_value=[]):
                with self.assertRaises(FileNotFoundError):
                    find_file("result.csv", local_dir, path)


if __name__ == "__main__":
    unittest.main()
