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

import sys
import json
import os
import argparse

# Set arguments for the tool
def setArgParse():
    # Setting the parser arguments
  parser = argparse.ArgumentParser(prog="ansible-check-builder",
                                   description="This script builds a check json file for the Sensu monitoring system.\n" +
                                               "\nIf using arguments only one check wil be created at a time\n" +
                                               "\n***NOTICE*** If using arguments option all arguments except version are required")
  parser.add_argument("-v", "--version", action='version', version='%(prog)s   2.0', help="Prints the tool version")
  parser.add_argument("-g", "--group", help="Ansible group")
  parser.add_argument("-n", "--name", help="The check's name")
  parser.add_argument("-c", "--command", help="The check's command to execute on the monitored machine")
  parser.add_argument("-i", "--interval", help="The check's interval time (seconds)")
  
  return (parser.parse_args())

# Write a dictionary to file
def writeToFile(jsCheckJson, strGroup, strCheckName):
  try:  
    # Creating a file and dumping the check's json
    fCheck=open(CHECK_PATH + strGroup + "/" + strCheckName + CHECK_EXTENSION, 'w+')
    json.dump(jsCheckJson, fCheck, indent=2, sort_keys=True)
    fCheck.close()
  except IOError as e:
    print "I/O error({0}): {1}".format(e.errno, e.strerror)

  # Print the check final json
  print json.dumps(jsCheckJson, indent=2, sort_keys=True)

def argsProvided(args, jsCheckJson):
  # Check if scripts directory for requested group exists and creates it if not
  if not os.path.exists(SCRIPTS_PATH + args.group):
    os.makedirs(SCRIPTS_PATH + args.group)

  # Check if scripts directory for requested group exists and creates it if not
  if not os.path.exists(CHECK_PATH + args.group):
    os.makedirs(CHECK_PATH + args.group)

  jsCheckJson['checks'][args.name]={}
  jsCheckJson['checks'][args.name]['command']=args.command
  jsCheckJson['checks'][args.name]['subscribers']=[]

  # Setting the subscribers
  jsCheckJson['checks'][args.name]['subscribers'].append(args.group)

  # Check if the user wants to add more subscribers
  bMoreSubscribers=raw_input("Do you want to add subscribers? [y/n] ")
  if (bMoreSubscribers == "y" or bMoreSubscribers == "yes"):
    # Get list of subscribers
    print "Enter subscibers names. For exit enter exit"    
    strSubscribers=raw_input()

    # While user didn't enter exit, subscribers will be added
    while (strSubscribers != "exit"):
      jsCheckJson['checks'][args.name]['subscribers'].append(strSubscribers)
      strSubscribers=raw_input()
  
  # Set the interval
  jsCheckJson['checks'][args.name]['interval']=int(args.interval)
  
  # Set the check standalone attribute to true
  jsCheckJson['checks'][args.name]['standalone']=bool(True)
  
  # Write the json to file
  writeToFile(jsCheckJson, args.group, args.name)
  
# This function creates a check json file based on execution time user input
def argsNotProvided(jsCheckJson): 
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

  # Setting the subscribers to the same as the ansible group
  jsCheckJson['checks'][strCheckName]['subscribers'].append(strAnsibleGroup)

  # Check if the user wants to add more subscribers
  bMoreSubscribers=raw_input("Do you want to add subscribers? [y/n] ")
  if (bMoreSubscribers == "y" or bMoreSubscribers == "yes"):
    # Get list of subscribers
    print "Enter subscibers names. For exit enter exit"    
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

  # Write the json to file
  writeToFile(jsCheckJson, strAnsibleGroup, strCheckName)
  
  # Clear the dictonary
  jsCheckJson['checks'].clear()


# ------------------------ Main -----------------------------
if __name__ == '__main__':
  # Initializing the default path variables
  CHECK_PATH="/etc/ansible/roles/sagyos.advanced.monitoring/checks/"
  SCRIPTS_PATH="/etc/ansible/roles/sagyos.advanced.monitoring/scripts/"
  CHECK_EXTENSION=".json"

  # Check if checks directory exists and creates it if not
  if not os.path.exists(CHECK_PATH):
    os.makedirs(CHECK_PATH)

  # Check if checks directory exists and creates it if not
  if not os.path.exists(SCRIPTS_PATH):
    os.makedirs(SCRIPTS_PATH)
    
  # Setting the parser arguments
  prArgs=setArgParse()

  # Creating check definition
  jsCheckJson={}
  jsCheckJson['checks']={}

  # Check if the user entered arguments
  if not len(sys.argv) > 1:
    # While user don't want to quit new checks will be created
    while True:
      # Building the check json and saves it
      argsNotProvided(jsCheckJson)

      strUserChoice=raw_input('Continue to another check? y/n: ')
    
      # Check if user want to exit
      if (strUserChoice == "n"):
        break
  elif not len(sys.argv) == 9:
    print "Please provide all the arguments except -v or --version"
  else:
    # Building the check json and saves it
    argsProvided(prArgs, jsCheckJson)
