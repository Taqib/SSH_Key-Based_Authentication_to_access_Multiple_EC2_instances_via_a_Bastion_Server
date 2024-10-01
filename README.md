SSH Key-Based Authentication to access Multiple EC2 instances via a Bastion Server
Overview
SSH (Secure Shell) is a protocol for securely connecting to remote systems over a network. Using public/private key pairs for authentication is a more secure method than password-based authentication.

We will work on a scenario like this, suppose we have four EC2 instances: one public-facing bastion server and three private server. We want to SSH into each private servers.

Before starting, why Use SSH Keys?
Enhanced Security: Passwords can be vulnerable, especially if they are weak or reused. SSH keys provide stronger authentication.

Convenience: Once set up, SSH keys allow you to log in to a server without needing to type a password.