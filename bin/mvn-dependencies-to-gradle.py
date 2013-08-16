#! /usr/bin/env python

import xml.etree.ElementTree as ET
import argparse
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

class Converter:

  def __init__(self, pom_file, parent = None, namespace = "{http://maven.apache.org/POM/4.0.0}"):
    self.xml_util = XMLUtil(namespace)
    self.pom = pom_file
    self.parent = parent
    pass

  def reset(self):
    self.versions = {}
    self.test_dependencies = []
    self.compile_dependencies = []
    self.runtime_dependencies = []
    self.system_dependencies = []
    self.provided_dependencies = []

  def printall():
    dependency_set = (
        self.test_dependencies,
        self.compile_dependencies,
        self.runtime_dependencies,
        self.system_dependencies,
        self.provided_dependencies)

    for dependencies in dependency_set:
      dependencies = sorted(dependencies)
      for dependency in dependencies:
        dependency.print_out()
      print ""

  def process_file(self):
    self.reset()

    xmldoc = ET.parse(self.pom)
    root = xmldoc.getroot()

    assert root is not None, root

    dependencyManagement = self.xml_util.find_one(root, 'dependencyManagement')
    if dependencyManagement is None or len(dependencyManagement) == 0:
      dependencyManagement = self.xml_util.find_one(root, 'dependencies')

    assert dependencyManagement is not None and \
      len(dependencyManagement) > 0, 'not a valid dependencyManagement node: %s' % dependencyManagement

    "we make an assumption that our first and only child is 'dependencies'"
    dependencies_element = dependencyManagement[0]
    dependencies = []

    print dependencies_element

    for dependency_element in dependencies_element:
      logging.info('dependency: %s', dependency_element.text)
      dependency = self.dependency_from_xml(dependency_element)
      logging.info(dependency)
      self.store_version(dependency.group_id, dependency.artifact_id, dependency.version)
      self.get_exclusions(dependency, dependency_element)
      getattr(self, '%s_dependencies' % (dependency.scope)).append(dependency)


  def get_exclusions(self, dependency, dependency_element):
    exclusions_element = self.xml_util.find_one(dependency_element, 'exclusion')

    if exclusions_element is not None:

      exclusions = self.xml_util.find_one(exclusions_element, 'exclusion')

      for exclusion in exclusions:
        exclusion_dependency = self.dependency_from_xml(exclusion, False)
        dependency.add_exclusion(exclusion_dependency)

  def dependency_from_xml(self, dependency_element, include_version=True):

    group_id = self.xml_util.find_one(dependency_element, 'groupId').text
    artifact_id = self.xml_util.find_one(dependency_element, 'artifactId').text
    scope = self.get_scope(dependency_element)
    
    if include_version:
      version = self.get_version_from_element(group_id, artifact_id, dependency_element)

    return Dependency(group_id, artifact_id, version, scope)


  def get_scope(self, dependency_element):

    scope_element = self.xml_util.find_one(dependency_element, 'scope')

    if scope_element is not None:
      return scope_element.text

    return 'compile'

  def get_version_from_element(self, group_id, artifact_id, dependency_element):
    version_element = self.xml_util.find_one(dependency_element, 'version')

    if version_element is None and self.parent:
      return parent.get_version(group_id, artifact_id)

    text = version_element.text

    if text.find('${') != -1 and text.find('}') != -1:
      return text.replace('.', '_')

    return text

  def store_version(self, group_id, artifact_id, version):
    key = self.make_version_key(group_id, artifact_id)
    self.versions[key] = version
      
  def get_version(self, group_id, artifact_id):
    key = self.make_version_key(group_id, artifact_id)

    if self.versions.has_key(key):
      return self.versions[key]

    raise Exception("%s not found in parent" % (key))

  def make_version_key(self, group_id, artifact_id):
    return '%s:%s' % (group_id, artifact_id)


class Dependency:

  def __init__(self, group_id, artifact_id, version, scope):
    self.group_id = group_id
    self.artifact_id = artifact_id
    self.version = version
    self.scope = scope
    self.prefix = 'testCompile' if scope == 'test' else scope
    self.exclusions = []
    
  def __str__(self):
    return self.dependency_str()

  def __cmp__(self, other):
    if self.prefix == other.prefix:
      return cmp(self.prefix, other.prefix)

    return cmp(self.prefix, other.prefix)

  def add_exclusion(self, exclusion):
    self.exclusions.add(exclusion)

  def dependency_str(self):
    return '%s:%s:%s' % (self.group_id, self.artifact_id, self.version)

  def print_out(self):

    if len(self.exclusions) == 0:
      print '%s "%s:%s:%s"' % (self.prefix, self.group_id, self.artifact_id, self.version)
    else:
      print '%s("%s:%s:%s") {' % (self.prefix, self.group_id, self.artifact_id, self.version)
      for exclusion in self.exclusions:
        print '  exclude group: "%s", module: "%s"' % (self.group_id, self.artifact_id)

      print '}'

class XMLUtil:

  def __init__(self, namespace):
    self.namespace = namespace

  def find_all(self, element, tag):
    return element.findall('%s%s' % (self.namespace, tag))

  def find_one(self, element, tag):
    found = self.find_all(element, tag)
    if len(found) > 0:
      return found[0]
    
    return None

  def find_tag_path(self, element, *tags):
    xpath_query = '/'
    for tag in tags:
      xpath_query += '%s%s/' % (self.namespace, tag)

    return element.findall(xpath_query)



def main():
  args = parse_arguments()

  if args.parent is not None:
    parent = Converter(args.parent)
    parent.process_file()

    current = Converter(args.pom, parent)
    current.process_file()
    current.printall()
  else:
    converter = Converter(args.pom)
    converter.process_file()
    converter.printall()


def parse_arguments():
  parser = argparse.ArgumentParser(description='Convert mvn dependencies to gradle dependencies')
  parser.add_argument('pom', help='The pom file to parse')
  parser.add_argument('-p', help='Parent Pom file', dest='parent', required=False)

  return parser.parse_args()

if __name__ == '__main__':
  main()
