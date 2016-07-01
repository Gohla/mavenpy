import os
from unittest import TestCase

from mavenpy.run import Maven

_DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')


class Test(TestCase):
  def test_maven_run(self):
    maven = Maven()
    maven.batch = True
    maven.debug = True
    maven.run_in_dir(_DATA_DIR, "clean", "verify")
