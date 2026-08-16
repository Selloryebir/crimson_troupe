import unittest

from scripts.validate_repository_policy import private_asset_violations


class ValidateRepositoryPolicyTest(unittest.TestCase):
    def test_accepts_public_metadata_and_mount_readme(self) -> None:
        paths = [
            "docs/background/02_crimson_troupe/04_collectibles/01_藏品.csv",
            "docs/background/02_crimson_troupe/04_collectibles/assets/collectibles/README.md",
        ]
        self.assertEqual(private_asset_violations(paths), [])

    def test_rejects_private_png_case_insensitively(self) -> None:
        paths = [
            "docs/background/02_crimson_troupe/04_collectibles/assets/collectibles/example.png",
            "docs/background/02_crimson_troupe/04_collectibles/assets/collectibles/EXAMPLE.PNG",
        ]
        self.assertEqual(private_asset_violations(paths), sorted(paths))

    def test_does_not_apply_to_unrelated_original_assets(self) -> None:
        paths = ["public/assets-original/project-owned.png"]
        self.assertEqual(private_asset_violations(paths), [])


if __name__ == "__main__":
    unittest.main()
