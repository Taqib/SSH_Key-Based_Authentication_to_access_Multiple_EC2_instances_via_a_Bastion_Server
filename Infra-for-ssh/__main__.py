import pulumi
import pulumi_aws as aws

# Create a VPC
vpc = aws.ec2.Vpc("my-vpc",
    cidr_block="10.0.0.0/16",
    tags={"Name": "my-vpc"}
)

# Export the VPC ID
pulumi.export("vpcId", vpc.id)

# Create a public subnet
public_subnet = aws.ec2.Subnet("public-subnet",
    vpc_id=vpc.id,
    cidr_block="10.0.1.0/24",
    availability_zone="ap-southeast-1a",
    map_public_ip_on_launch=True,
    tags={"Name": "public-subnet"}
)

# Export the public subnet ID
pulumi.export("publicSubnetId", public_subnet.id)

# Create a private subnet
private_subnet = aws.ec2.Subnet("private-subnet",
    vpc_id=vpc.id,
    cidr_block="10.0.2.0/24",
    availability_zone="ap-southeast-1a",
    tags={"Name": "private-subnet"}
)

# Export the private subnet ID
pulumi.export("privateSubnetId", private_subnet.id)

# Create an Internet Gateway
igw = aws.ec2.InternetGateway("internet-gateway",
    vpc_id=vpc.id,
    tags={"Name": "IGW"}
)

# Export the Internet Gateway ID
pulumi.export("igwId", igw.id)

# Create a route table for the public subnet
public_route_table = aws.ec2.RouteTable("public-route-table",
    vpc_id=vpc.id,
    tags={"Name": "rt-public"}
)

# Create a route in the route table for the Internet Gateway
route = aws.ec2.Route("igw-route",
    route_table_id=public_route_table.id,
    destination_cidr_block="0.0.0.0/0",
    gateway_id=igw.id
)

# Associate the route table with the public subnet
route_table_association = aws.ec2.RouteTableAssociation("public-route-table-association",
    subnet_id=public_subnet.id,
    route_table_id=public_route_table.id
)

# Export the public route table ID
pulumi.export("publicRouteTableId", public_route_table.id)

# Allocate an Elastic IP for the NAT Gateway
eip = aws.ec2.Eip("nat-eip", vpc=True)

# Create the NAT Gateway
nat_gateway = aws.ec2.NatGateway("nat-gateway",
    subnet_id=public_subnet.id,
    allocation_id=eip.id,
    tags={"Name": "NGW"}
)

# Export the NAT Gateway ID
pulumi.export("natGatewayId", nat_gateway.id)

# Create a route table for the private subnet
private_route_table = aws.ec2.RouteTable("private-route-table",
    vpc_id=vpc.id,
    tags={"Name": "rt-private"}
)

# Create a route in the route table for the NAT Gateway
private_route = aws.ec2.Route("nat-route",
    route_table_id=private_route_table.id,
    destination_cidr_block="0.0.0.0/0",
    nat_gateway_id=nat_gateway.id
)

# Associate the route table with the private subnet
private_route_table_association = aws.ec2.RouteTableAssociation("private-route-table-association",
    subnet_id=private_subnet.id,
    route_table_id=private_route_table.id
)

# Export the private route table ID
pulumi.export("privateRouteTableId", private_route_table.id)

# Create a security group for the public instance (Bastion Server)
public_security_group = aws.ec2.SecurityGroup("public-secgrp",
    vpc_id=vpc.id,
    description="Enable HTTP and SSH access for public instance",
    ingress=[
        aws.ec2.SecurityGroupIngressArgs(
            protocol="tcp",
            from_port=80,
            to_port=80,
            cidr_blocks=["0.0.0.0/0"]
        ),
        aws.ec2.SecurityGroupIngressArgs(
            protocol="tcp",
            from_port=22,
            to_port=22,
            cidr_blocks=["0.0.0.0/0"]
        )
    ],
    egress=[
        aws.ec2.SecurityGroupEgressArgs(
            protocol="-1",
            from_port=0,
            to_port=0,
            cidr_blocks=["0.0.0.0/0"]
        )
    ]
)

# Use the specified Ubuntu 24.04 LTS AMI
ami_id = "ami-060e277c0d4cce553"

# Create an EC2 instance in the public subnet (Bastion Server)
public_instance = aws.ec2.Instance("bastion-instance",
    instance_type="t2.micro",
    vpc_security_group_ids=[public_security_group.id],
    ami=ami_id,
    subnet_id=public_subnet.id,
    key_name="BastionServer",
    associate_public_ip_address=True,
    tags={"Name": "Bastion-Server"}
)

# Export the public instance ID and IP
pulumi.export("publicInstanceId", public_instance.id)
pulumi.export("publicInstanceIp", public_instance.public_ip)

# Create a security group for the private instances allowing SSH only from the bastion server
private_security_group = aws.ec2.SecurityGroup("private-secgrp",
    vpc_id=vpc.id,
    description="Allow SSH access from Bastion server",
    ingress=[
        aws.ec2.SecurityGroupIngressArgs(
            protocol="tcp",
            from_port=22,
            to_port=22,
            cidr_blocks=[pulumi.Output.concat(public_instance.private_ip, "/32")]
        )
    ],
    egress=[
        aws.ec2.SecurityGroupEgressArgs(
            protocol="-1",
            from_port=0,
            to_port=0,
            cidr_blocks=["0.0.0.0/0"]
        )
    ]
)

# Create EC2 instances in the private subnet
private_instance1 = aws.ec2.Instance("private-instance1",
    instance_type="t2.micro",
    vpc_security_group_ids=[private_security_group.id],
    ami=ami_id,
    subnet_id=private_subnet.id,
    key_name="PrivateServer1",
    tags={"Name": "Private-server1"}
)

# Export the private instance 1 ID and private IP
pulumi.export("privateInstance1Id", private_instance1.id)
pulumi.export("privateInstance1PrivateIp", private_instance1.private_ip)

private_instance2 = aws.ec2.Instance("private-instance2",
    instance_type="t2.micro",
    vpc_security_group_ids=[private_security_group.id],
    ami=ami_id,
    subnet_id=private_subnet.id,
    key_name="PrivateServer2",
    tags={"Name": "Private-server2"}
)

# Export the private instance 2 ID and private IP
pulumi.export("privateInstance2Id", private_instance2.id)
pulumi.export("privateInstance2PrivateIp", private_instance2.private_ip)

private_instance3 = aws.ec2.Instance("private-instance3",
    instance_type="t2.micro",
    vpc_security_group_ids=[private_security_group.id],
    ami=ami_id,
    subnet_id=private_subnet.id,
    key_name="PrivateServer3",
    tags={"Name": "Private-server3"}
)

# Export the private instance 3 ID and private IP
pulumi.export("privateInstance3Id", private_instance3.id)
pulumi.export("privateInstance3PrivateIp", private_instance3.private_ip)
