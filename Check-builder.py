import json

# Variables deffinition
CHECK_PATH="C:\\Temp\\"
CHECK_EXTENSION=".json"

# Creating check definition
jsCheckJson={}
jsCheckJson['checks']={}

# While user don't want to quit new checks will be created
while True:
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

  try:
    # Check if check is stand alone
    bIsStandalone=raw_input("Is standalone? (true/false) [t/f]: ")

    # Check if user entered t or f
    if (bIsStandalone == "t"):
      bIsStandalone=True
    elif(bIsStandalone == "f"):
      bIsStandalone=False

    jsCheckJson['checks'][strCheckName]['standalone']=bool(bIsStandalone)
  except ValueError:
    print("Please enter boolean")

  try:  
    # Creating a file and dumping the check's json
    fCheck=open(CHECK_PATH + strCheckName + CHECK_EXTENSION, 'w+')
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