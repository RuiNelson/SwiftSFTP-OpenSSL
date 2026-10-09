import importlib.util
from pathlib import Path
import unittest

SCRIPT = Path(__file__).resolve().parents[2] / "Scripts/check-openssl-release.py"
SPEC = importlib.util.spec_from_file_location("release_check", SCRIPT)
release_check = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(release_check)


class ReleaseCheckTests(unittest.TestCase):
    def test_stable_selection_ignores_prereleases_and_peeled_refs(self):
        refs = "\n".join(f"{'a' * 40}\trefs/tags/{tag}" for tag in [
            "openssl-3.5.99", "openssl-4.0.9", "openssl-4.0.10",
            "openssl-4.1.0-alpha1", "openssl-4.1.0-beta2", "openssl-4.1.0-dev",
            "openssl-4.0.10^{}", "unrelated-tag",
        ])
        self.assertEqual(release_check.latest_stable_tag(refs), "openssl-4.0.10")

    def test_missing_stable_releases_fail(self):
        with self.assertRaises(ValueError):
            release_check.latest_stable_tag("a refs/tags/openssl-4.1.0-beta2")

    def test_open_and_closed_issues_both_prevent_duplicates(self):
        marker = "<!-- swiftsftp-openssl-release:openssl-4.0.4 -->"
        for state in ["open", "closed"]:
            with self.subTest(state=state):
                pages = [[{"body": "Other release", "state": "open"}],
                         [{"body": marker, "state": state}]]
                self.assertTrue(release_check.already_reported(pages, marker))

    def test_pull_requests_and_other_releases_do_not_suppress_issues(self):
        marker = "<!-- swiftsftp-openssl-release:openssl-4.0.4 -->"
        pages = [[{"body": marker, "pull_request": {}},
                  {"body": "<!-- swiftsftp-openssl-release:openssl-4.0.3 -->"},
                  {"body": None}]]
        self.assertFalse(release_check.already_reported(pages, marker))


if __name__ == "__main__":
    unittest.main()
