import os
import unittest

from shutil import which
from mavenpy.run import Maven

_DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')


class Test(unittest.TestCase):
  def test_maven_run(self):
    print("test_maven_run")
    maven = Maven()
    maven.batch = True
    maven.debug = True
    maven.run_in_dir(_DATA_DIR, "clean", "verify")

  @unittest.skipIf(which("mvnd") == None,
                   "requires mvnd command on path")
  def test_maven_daemon_run(self):
    print("test_maven_daemon_run")
    maven = Maven()
    maven.batch = True
    maven.debug = True
    maven.daemon = True
    maven.run_in_dir(_DATA_DIR, "clean", "verify")

  def test_maven_version(self):
    print("test_maven_version")
    maven = Maven()
    v = maven.get_version()
    self.assertNotEqual("", v)    # e.g., "3.6.0"

if __name__ == '__main__':
    unittest.main()