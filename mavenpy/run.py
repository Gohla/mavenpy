import os
import subprocess
import re
from shutil import which


class Maven(object):
  def __init__(self):
    self.targets = []
    self.properties = {}
    self.extraArgs = []

    self.settingsFile = None
    self.globalSettingsFile = None
    self.localRepo = None

    self.profiles = []

    self.skipTests = False

    self.noSnapshotUpdates = False
    self.forceSnapshotUpdate = False
    self.offline = False

    self.batch = False
    self.debug = False
    self.errors = False
    self.quiet = False

    self.opts = None
    self.env = {}

  def run_in_dir(self, cwd, *extraTargets, **extraProperties):
    self.run(cwd, None, *extraTargets, **extraProperties)

  def run_on_file(self, buildFile, *extraTargets, **extraProperties):
    self.run(None, buildFile, *extraTargets, **extraProperties)

  def run(self, cwd, buildFile, *extraTargets, **extraProperties):
    args = []

    path = which('mvn')
    if path:
      args.append(path)
    else:
      raise RuntimeError("Cannot run Maven, executable not found on the path")

    if buildFile:
      args.append('--file "{}"'.format(buildFile))

    if self.settingsFile:
      args.append('--settings "{}"'.format(self.settingsFile))
    if self.globalSettingsFile:
      args.append('--global-settings "{}"'.format(self.globalSettingsFile))
    if self.localRepo:
      args.append('-Dmaven.repo.local="{}"'.format(self.localRepo))

    if len(self.profiles) != 0:
      args.append('--activate-profiles={}'.format(','.join(self.profiles)))

    if self.skipTests:
      args.append('-Dmaven.test.skip=true')
      args.append('-DskipTests=true')

    if self.noSnapshotUpdates:
      args.append('--no-snapshot-updates')
    if self.forceSnapshotUpdate:
      args.append('--update-snapshots')
    if self.offline:
      args.append('--offline')

    if self.batch:
      args.append('--batch-mode')
    if self.debug:
      args.append('--debug')
    if self.errors:
      args.append('--errors')
    if self.quiet:
      args.append('--quiet')

    allProperties = {}
    allProperties.update(self.properties)
    allProperties.update(extraProperties)
    for name, value in allProperties.items():
      args.append('-D{}={}'.format(name, value))

    allTargets = []
    allTargets.extend(self.targets)
    allTargets.extend(extraTargets)
    args.extend(allTargets)

    if self.extraArgs:
      args.extend(self.extraArgs)

    env = os.environ.copy()
    if self.opts:
      env['MAVEN_OPTS'] = self.opts
    env.update(self.env)

    cmd = ' '.join(args)
    if self.opts:
      print('MAVEN_OPTS="{}" {}'.format(self.opts, cmd))
    else:
      print(cmd)
    try:
      process = subprocess.Popen(cmd, cwd=cwd, env=env, shell=True)
      process.communicate()
      if process.returncode != 0:
        raise RuntimeError("Maven run failed")
    except KeyboardInterrupt:
      raise RuntimeError("Maven run interrupted")

  versionRegex = re.compile(r"\s*Apache\s+Maven\s+([\d\.]+)")

  def get_version(self, cwd=None):
    args = []

    path = which('mvn')
    if path:
      args.append(path)
    else:
      raise RuntimeError("Cannot run Maven, executable not found on the path")

    args.append('--version')
    
    env = os.environ.copy()
    if self.opts:
      env['MAVEN_OPTS'] = self.opts
    env.update(self.env)

    cmd = ' '.join(args)
    if self.opts:
      print('MAVEN_OPTS="{}" {}'.format(self.opts, cmd))
    else:
      print(cmd)
    try:
      process = subprocess.Popen(cmd, cwd=cwd, env=env, shell=True, stdout=subprocess.PIPE)

      firstLine = process.stdout.readline().decode('utf-8').rstrip()

      process.communicate()

      if process.returncode != 0:
        raise RuntimeError("Maven command failed")
      if not firstLine:
        raise RuntimeError("Maven command did not print anything")
      return self.versionRegex.search(firstLine).group(1)
    except KeyboardInterrupt:
      raise RuntimeError("Maven command interrupted")