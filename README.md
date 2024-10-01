SSH Key-Based Authentication to access Multiple EC2 instances via a Bastion Server
Overview
SSH (Secure Shell) is a protocol for securely connecting to remote systems over a network. Using public/private key pairs for authentication is a more secure method than password-based authentication.

We will work on a scenario like this, suppose we have four EC2 instances: one public-facing bastion server and three private server. We want to SSH into each private servers.

Before starting, why Use SSH Keys?
Enhanced Security: Passwords can be vulnerable, especially if they are weak or reused. SSH keys provide stronger authentication.

Convenience: Once set up, SSH keys allow you to log in to a server without needing to type a password.

Create Infrastructure(Optional if you have your servers up and running)
For this setup, we will need a Publicly accessible Bastion server, and three private servers. We can create these servers in AWS. We can manually create the servers by login in to the AWS management console or we can create the servers and other necessary resouces using PULUMI or Terraform. In this lab, we will use PULUMI Python as Infrastructure as code.

Create a Key Pair for your SERVER's:

We will use specific keys for SSHing into servers. So, we have to create 4 key pairs as we have 4 servers. This is for more secure connection. You can also create a single key pair as well.

Bastion-server key generation

"aws ec2 create-key-pair --key-name BastionServer --query 'KeyMaterial' --output text > BastionServer.pem
chmod 400 BastionServer.pem
"
Private-server1 key generation

"aws ec2 create-key-pair --key-name PrivateServer1 --query 'KeyMaterial' --output text > PrivateServer1.pem
chmod 400 PrivateServer1.pem
"

Private-server2 key generation

"aws ec2 create-key-pair --key-name PrivateServer2 --query 'KeyMaterial' --output text > PrivateServer2.pem
chmod 400 PrivateServer2.pem
"

Private-server3 key generation

"aws ec2 create-key-pair --key-name PrivateServer3 --query 'KeyMaterial' --output text > PrivateServer3.pem
chmod 400 PrivateServer3.pem
"

NOTE: Make sure to set the correct permission for the keys

Traditional way: SSH into the private instances via Bastion server
When using the direct SSH command, you have to typically do something like this

Copy the Key files from your local directory to Bastion Server:
"scp -i BastionServer.pem PrivateServer1.pem PrivateServer2.pem PrivateServer3.pem privateubuntu@<bastion-public-ip>:~/.ssh/"

SSH into the Bastion Server to check the files:
"ssh -i BastionServer.pem ubuntu@<bastion-public-ip>"

This command will securely copy the key files into Bastion server using the bastion server key file. After copying the file make sure to set the correct file permission.

Change the file permission of the key files in the bastion server:

"chmod 400 PrivateServer1.pem
chmod 400 PrivateServer2.pem
chmod 400 PrivateServer3.pem
"

Then, SSH from the Bastion Server to a Private Instances:

private-server1

"ssh -i ~/.ssh/PrivateServer1.pem ubuntu@<private-instance1-ip>"

private-server2

"ssh -i ~/.ssh/PrivateServer2.pem ubuntu@<private-instance2-ip>"

private-server3
"ssh -i ~/.ssh/PrivateServer3.pem ubuntu@<private-instance3-ip>"

Set the hostname of the servers(Optional)
You can set the hostname of the servers by these commands:

Bastion Server
"sudo hostnamectl set-hostname bastion-server"

Private Server 1
"sudo hostnamectl set-hostname private-server1"

Private Server 2
"sudo hostnamectl set-hostname private-server2"

Private Server 3
"sudo hostnamectl set-hostname private-server3"

You can again ssh into the servers to check if hostname is correctly setup or not.

Issues with This Approach:
Repetitive Commands: Every time you want to SSH into a private instance, you have to manually SSH into the bastion server first, then SSH into the private instance. This involves typing long commands repeatedly.

Private Key Management: You must specify the private key with the -i option every time, which can be cumbersome if you manage multiple keys for different instances.

Multi-Hop SSH: SSHing into private instances requires a multi-hop process, where you first connect to the bastion server and then hop to the private instances. This is not only tedious but also error-prone.

Simplifying with an SSH Config File
You can solve these issues by configuring the ~/.ssh/config file. This file allows you to define shortcuts and advanced SSH options, making the SSH process smoother and more efficient.


Step 1: Set Up the SSH Config File
Create a config file in the ~/.ssh/ directory. Here’s an example config file that simplifies the SSH process for this scenario:

NOTE:

Configure the HostName with correct IP or DNS name.
User is ubuntu by default if your have launched an ubuntu instance. Change accordingly to your requirement.
Make sure to change the location of your key files accordingly.

Explanation of the Config File:
Host bastion: This section defines the connection to your bastion server. The HostName is the public IP of the bastion server, and IdentityFile specifies the private key used for authentication.

Host private-instance-X: These sections define the connection to each private instance. The ProxyJump bastion directive tells SSH to first connect to the bastion server before connecting to the private instance.
