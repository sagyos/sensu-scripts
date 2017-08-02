# Author - Sagi Yosef
# Creation Date 30.07.2017
#
# This script builds sensu check json file by user input.
#
# --- HOW TO RUN ---
# Copy the script to the ansible server and run the script
#
# python check-json-builder-standalone.py
#
# *** Notice you have to install python ***

import json
import os

CHECK_PATH="/etc/ansible/roles/sagyos.advanced.monitoring/checks/"
SCRIPTS_PATH="/etc/ansible/roles/sagyos.advanced.monitoring/scripts/"
CHECK_EXTENSION=".json"

# Check if checks directory exists and creates it if not
if not os.path.exists(CHECK_PATH):
  os.makedirs(CHECK_PATH)

# Check if checks directory exists and creates it if not
if not os.path.exists(SCRIPTS_PATH):
  os.makedirs(SCRIPTS_PATH)

# Creating check definition
jsCheckJson={}
jsCheckJson['checks']={}

# While user don't want to quit new checks will be created
while True:
  # Get ansible monitored group
  strAnsibleGroup=raw_input("Enter the ansible group name (must be the same): ")
  
  # Check if scripts directory for requested group exists and creates it if not
  if not os.path.exists(SCRIPTS_PATH + strAnsibleGroup):
    os.makedirs(SCRIPTS_PATH + strAnsibleGroup)

  # Check if scripts directory for requested group exists and creates it if not
  if not os.path.exists(CHECK_PATH + strAnsibleGroup):
    os.makedirs(CHECK_PATH + strAnsibleGroup)

  # Get the checks uniqe name
  strCheckName=raw_input("Enter check uniqe name: ")
  jsCheckJson['checks'][strCheckName]={}

  # Get checks command
  print "Enter the check's command"
  print "-------------------------"
  jsCheckJson['checks'][strCheckName]['command']=raw_input()
  jsCheckJson['checks'][strCheckName]['subscribers']=[]

  # Get list of subscribers
  print "Enter subscribers. \nFor exit press exit"
  strSubscribers=raw_input()

  # While user didn't enter exit, subscribers will be added
  while (strSubscribers != "exit"):
    jsCheckJson['checks'][strCheckName]['subscribers'].append(strSubscribers)
    strSubscribers=raw_input()

  # Getting the checks interval
  while True:
    try:
      # Get checks interval time in seconds
      jsCheckJson['checks'][strCheckName]['interval']=int(raw_input("Enter interval time (seconds): "))
    except ValueError:
      print("Please enter integer")
      continue
    else:
      # Interval was successfully parsed!
      break

  # Set the check standalone attribute to true
  jsCheckJson['checks'][strCheckName]['standalone']=bool(True)

  try:  
    # Creating a file and dumping the check's json
    fCheck=open(CHECK_PATH + strAnsibleGroup + "/" + strCheckName + CHECK_EXTENSION, 'w+')
    json.dump(jsCheckJson, fCheck, indent=2, sort_keys=True)
    fCheck.close()
  except IOError as e:
    print "I/O error({0}): {1}".format(e.errno, e.strerror)

  # Print the check final json
  print json.dumps(jsCheckJson, indent=2, sort_keys=True)
  
  # Clear the dictonary
  jsCheckJson['checks'].clear()

  strUserChoice=raw_input('Continue to another check? y/n: ')

  # Check if user want to exit
  if (strUserChoice == "n"):
    break