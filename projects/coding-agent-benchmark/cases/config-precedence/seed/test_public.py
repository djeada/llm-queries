import unittest

from config import load_config


class ConfigTests(unittest.TestCase):
    def test_defaults(self):
        self.assertEqual(
            load_config(),
            {"host": "127.0.0.1", "port": 8000, "debug": False},
        )

    def test_file_values_override_defaults(self):
        self.assertEqual(load_config({"host": "file"})["host"], "file")

    def test_environment_parses_types(self):
        result = load_config(
            env={"APP_PORT": "9100", "APP_DEBUG": "YES"}
        )
        self.assertEqual(result["port"], 9100)
        self.assertIs(result["debug"], True)


if __name__ == "__main__":
    unittest.main()
