try:
    import boto
except ImportError:
    print "Error, must install boto (i.e. sudo pip install boto)"
import sys
import boto.ec2


if len(sys.argv) != 2 and len(sys.argv) != 4:
    print "Usage: python terminate.py instance_id \nOR\n python terminate.py instance_id AWS_key_id AWS_access_key"
    exit()
    
instance_id = sys.argv[1]


print "Connecting to AWS us-east-1"
#connect to AWS
if len(sys.argv) == 4:
    conn = boto.ec2.connect_to_region("us-east-1", aws_access_key_id=sys.argv[2], aws_secret_access_key=sys.argv[3])
else:
    conn = boto.ec2.connect_to_region("us-east-1") #id and key set up in boto environment

#check if connection was successful
if not conn:
    print "Error: Failed to connect to region, exiting..."
    exit()
else:
    print "Successfully connected"


print "Terminating..."
term = conn.terminate_instances(instance_ids=[instance_id], dry_run=False)
if len(term) > 0:
    print "complete, terminated: "
    print term[0]
else:
    print "failed, no instance terminated"