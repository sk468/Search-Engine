The setup and termination scripts can be run as follows:

a. If the boto environment on the computer is set up with a key id and access key:
	python setup.py
	python terminate.py instance_id

b. If the boto envirnoment is not set up on the computer:
	python setup.py instance_id AWS_key_id AWS_access_key
	python terminate.py instance_id instance_id AWS_key_id AWS_access_key

The scripts are run through python and require the following 3rd party libraries:

	boto

	paramiko (setup only, used for ssh connection)

If the above are not installed, the script will exit, instructing you to install the missing library

The script requires the following external file(s):

	rocketeer.zip

This file contains everything needed to run the rocketeer frontend and is copied to the AWS server. 
