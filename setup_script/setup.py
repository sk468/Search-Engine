try:
    import boto
except ImportError:
    print "Error, must install boto (i.e. sudo pip install boto)"
    exit()
import boto.ec2
import time
try: 
    import paramiko
except ImportError:
    print "Error, must install paramiko (i.e. sudo pip install paramiko)"
    exit()
import os
import os.path
import socket
import sys

cwd = os.getcwd()


frontend_zip = "rocketeer.zip"
frontend_filename = "rocketeer.zip"
keypair_name = "rocketeer_key"
keypair_file = keypair_name + ".pem"
security_group_name = "rocketeer_security"

#connect to AWS
if len(sys.argv) != 1 and len(sys.argv) != 3:
    print "Usage: python terminate.py \nOR\n python terminate.py AWS_key_id AWS_access_key"
    exit()
    
print "Connecting to AWS us-east-1"
#connect to AWS
if len(sys.argv) == 3:
    conn = boto.ec2.connect_to_region("us-east-1", aws_access_key_id=sys.argv[1], aws_secret_access_key=sys.argv[2])
else:
    conn = boto.ec2.connect_to_region("us-east-1") #id and key set up in boto environment


if not conn:
    print "Error: Failed to connect to region, exiting..."
    exit()
else:
    print "Successfully connected to Amazon"


#set up keypair for ssh
print "Getting keypair"
keypair = conn.get_key_pair(keypair_name, dry_run=False)
if keypair: #keypair does not yet exist
    keypair.delete(dry_run=False)

keypair = conn.create_key_pair(keypair_name, dry_run=False)

if os.path.isfile(keypair_file):
    os.remove(keypair_file)
keypair.save(cwd)

print "Creating security group"

#create security group and set up ports for ssh & http
secg = None
try: 
    secg = conn.get_all_security_groups(groupnames=[security_group_name], dry_run=False)[0]
except:
    secg = conn.create_security_group(security_group_name, "Rocketeer security group", "", dry_run=False)
    secg.authorize("ICMP", -1, -1, '0.0.0.0/0')
    secg.authorize("TCP", 22, 22, '0.0.0.0/0')
    secg.authorize("TCP", 80, 80, '0.0.0.0/0')



    
    
print "starting an AWS instance"
#create an instance
all_instances = conn.run_instances(image_id='ami-88aa1ce0', min_count=1, max_count=1, key_name=keypair_name, security_groups=[security_group_name], instance_type="t1.micro")

#ensure the instance starts up as expected
instance = all_instances.instances[0]
time.sleep(10)
while instance.update() != 'running':
    time.sleep(5)

#output instance information
print "\n new AWS ec2 instance set up"
print "\n\nIP address of instance:"
print instance.ip_address
print "\n\nID of instance:"
print instance.id
ip_addr = instance.ip_address


print "\n\n waiting for server to accept ssh connection"

time.sleep(30)


key = paramiko.RSAKey.from_private_key_file(keypair_file)
#key = paramiko.RSAKey.from_private_key_file('default.pem')
c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
print "connecting to ec2 instance"

while True:
    try : 
        c.connect( hostname = ip_addr, username = "ubuntu", pkey = key )
    except paramiko.ssh_exception.NoValidConnectionsError:
        print "no valid connection, ssh connection not available yet, will try again in 30 seconds"
        time.sleep(30)
        continue
    except paramiko.ssh_exception.AuthenticationException:
        print "authentication exception, problem with authorization key, try delete pem file and retry"
        exit()
    break
    
    

print "connected to ec2 instance: ", ip_addr
#copy over files
sftp = c.open_sftp()
sftp.put(frontend_zip, frontend_zip)
sftp.close()

#install needed libraries and tools, unzip file, run instance
commands = [ "sudo apt-get update",
             "sudo apt-get install zip -y",
             "unzip -o " + frontend_filename + " -d front",
             "sudo apt-get install python-setuptools python-dev build-essential -y",
             "sudo easy_install pip",
             "sudo pip install bottle",
             "sudo pip install sympy",
            "cd front/rocketeer; nohup sudo python frontend_rocketeer.py " + ip_addr + " >/dev/null 2>&1  &",
           ]
for command in commands:
    print "Executing {}".format( command )
    print "May take a few minutes, please be patient"
    stdin , stdout, stderr = c.exec_command(command)
    print stdout.read()
    print( "Errors")
    print stderr.read()
    
print "\nRocketeer now running on server at ", ip_addr
print "\nID of instance: "
print instance.id

#allow user to close session
raw_input("Press Enter to close connection, instance will continue to run...")   
    
c.close()

#deleting keypair file
if os.path.isfile(keypair_file):
    os.remove(keypair_file)
