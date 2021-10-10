#! /usr/bin/python3

import os
import json
import subprocess

DIR = os.getcwd()
HOME = os.path.expanduser('~')

def run(cmd):
  process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  return process.communicate()[0].decode("utf-8")

with open('package.json') as f:
  text = f.read()
  package = json.loads(text)

for package_name, v_now in package['dependencies'].items():
  if not package_name.startswith('@unrest'):
    continue
  v_now = v_now.replace('^', '')
  with open(os.path.join(HOME, 'projects', package_name, 'package.json')) as f:
    v_new = json.loads(f.read())['version']
  if v_now != v_new:
    print(f'{package_name} is behind: {v_now} vs {v_new}')

  os.chdir(os.path.join(HOME, 'projects', package_name))
  stdout = run(['git', 'log', '--pretty=format:"%h: %s"', '-10'])
  for commit_no, line in enumerate(stdout.split('\n')):
    if v_new in line:
      break
  if commit_no != 0:
    print(f'\npublished version of {package_name} may be {commit_no} commits behind')
    print('\n'.join(stdout.split('\n')[:commit_no+1]))

  stdout = run(['git', 'status', '--porcelain'])
  if stdout:
    print(f'{package_name} has uncommitted code')
    print(stdout)