import os
import unittest

from mavenpy.run import Maven

_DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')


class Test(unittest.TestCase):
  def test_maven_run(self):
    maven = Maven()
    maven.batch = True
    maven.debug = True
    maven.run_in_dir(_DATA_DIR, "clean", "verify")

  def test_maven_version(self):
    maven = Maven()
    v = maven.get_version()
    self.assertNotEqual("", v)    # e.g., "3.6.0"

if __name__ == '__main__':
    unittest.main()