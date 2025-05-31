import unittest

from gen_utils import *

class TestGenUtils(unittest.TestCase):
    def test_title_extract(self):
        self.assertEqual("Hello", extract_title("# Hello"))

    def test_title_extract_multi(self):
        md = """
# Title

# Not a title
"""
        self.assertEqual("Title", extract_title(md))

    def test_title_extract_lower(self):
        md = """
Random text

**more**

# Title

Hi
"""
        self.assertEqual("Title", extract_title(md))

    def test_title_extract_exception(self):
        self.assertRaises(Exception, extract_title, "No title here")

    def test_title_extract_space(self):
        self.assertEqual("Test", extract_title("#     Test"))
