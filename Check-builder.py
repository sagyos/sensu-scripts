import json

# Variables deffinition
CHECK_PATH="C:\\Temp\\"
CHECK_EXTENSION=".json"

# Creating check definition
jsCheckJson={}
jsCheckJson['checks']={}

# Get the checks uniqe name
print "Enter check uniqe name"
strCheckName=raw_input()
jsCheckJson['checks'][strCheckName]={}

# Get checks command
print "Enter the check's command"
jsCheckJson['checks'][strCheckName]['command']=raw_input()
jsCheckJson['checks'][strCheckName]['subscribers']=[]

# Get list of subscribers
print "Enter subscribers. For exit press exit"
strSubscribers=raw_input()

# While user didn't enter exit, subscribers will be added
while (strSubscribers != "exit"):
  jsCheckJson['checks'][strCheckName]['subscribers'].append(strSubscribers)
  strSubscribers=raw_input()

# Get checks interval time in seconds
print "Enter interval time (seconds)"
jsCheckJson['checks'][strCheckName]['interval']=int(raw_input())

# Check if check is stand alone
print "Is standalone? (true/false) [t/f]"
bIsStandalone=raw_input()

# Check if user entered t or f
if (bIsStandalone == "t"):
  bIsStandalone=True
elif(bIsStandalone == "f"):
  bIsStandalone=False

jsCheckJson['checks'][strCheckName]['standalone']=bool(bIsStandalone)

# Creating a file and dumping the check's json
fCheck=open(CHECK_PATH + strCheckName + CHECK_EXTENSION, 'w+')
json.dump(jsCheckJson, fCheck, indent=2, sort_keys=True)
fCheck.close()

# Print the check final json
print json.dumps(jsCheckJson, indent=2, sort_keys=True)