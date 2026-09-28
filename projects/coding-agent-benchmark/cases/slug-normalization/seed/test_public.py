import unittest

from slugify import slugify


class SlugifyTests(unittest.TestCase):
    def test_simple_words(self):
        self.assertEqual(slugify("Hello World"), "hello-world")

    def test_lowercase(self):
        self.assertEqual(slugify("ReleaseNotes"), "releasenotes")


if __name__ == "__main__":
    unittest.main()
