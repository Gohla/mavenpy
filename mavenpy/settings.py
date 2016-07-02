import os

import pystache


class MavenSettingsGenerator(object):
  def __init__(self, location=None, repositories=None, mirrors=None):
    self.location = location or MavenSettingsGenerator.user_settings_location()
    self.repositories = repositories or []
    self.mirrors = mirrors or []

  def generate(self):
    profileDict = {}
    for repo in self.repositories:
      profileId, repoId, url, layout, releases, snapshots, plugins = repo
      if profileId not in profileDict:
        profileDict[profileId] = []
      profileDict[profileId].append({
        'id'       : repoId,
        'url'      : url,
        'layout'   : layout,
        'releases' : str(releases).lower(),
        'snapshots': str(snapshots).lower(),
        'plugins'  : plugins
      })

    profileObjects = []
    for profileId, repos in profileDict.items():
      profileObjects.append({'profileId': profileId, 'repos': repos})

    mirrorObjects = []
    for mirror in self.mirrors:
      mirrorId, url, mirrorOf = mirror
      mirrorObjects.append({'id': mirrorId, 'url': url, 'mirrorOf': mirrorOf})

    settingsTemplate = '''<?xml version="1.0" ?>
  <settings xmlns="http://maven.apache.org/SETTINGS/1.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://maven.apache.org/SETTINGS/1.0.0 http://maven.apache.org/xsd/settings-1.0.0.xsd">
    <profiles>
      {{#profiles}}
      <profile>
        <id>{{profileId}}</id>
        <activation>
          <activeByDefault>true</activeByDefault>
        </activation>
        <repositories>
          {{#repos}}
          <repository>
            <id>{{id}}</id>
            <url>{{url}}</url>
            {{#layout}}<layout>{{layout}}</layout>
            {{/layout}}<releases>
              <enabled>{{releases}}</enabled>
            </releases>
            <snapshots>
              <enabled>{{snapshots}}</enabled>
            </snapshots>
          </repository>
          {{/repos}}
        </repositories>
        <pluginRepositories>
          {{#repos}}{{#plugins}}<pluginRepository>
            <id>{{id}}</id>
            <url>{{url}}</url>
            {{#layout}}<layout>{{layout}}</layout>
            {{/layout}}<releases>
              <enabled>{{releases}}</enabled>
            </releases>
            <snapshots>
              <enabled>{{snapshots}}</enabled>
            </snapshots>
          </pluginRepository>{{/plugins}}{{/repos}}
        </pluginRepositories>
      </profile>
      {{/profiles}}
    </profiles>
    <mirrors>
      {{#mirrors}}
      <mirror>
        <id>{{id}}</id>
        <url>{{url}}</url>
        <mirrorOf>{{mirrorOf}}</mirrorOf>
      </mirror>
      {{/mirrors}}
    </mirrors>
  </settings>
  '''

    settingsXml = pystache.render(settingsTemplate, {'profiles': profileObjects, 'mirrors': mirrorObjects})
    print('Setting contents of {} to:\n{}'.format(self.location, settingsXml))
    with open(self.location, "w") as settingsFile:
      settingsFile.write(settingsXml)

  @staticmethod
  def user_settings_location():
    return os.path.join(os.path.expanduser('~'), '.m2/settings.xml')
