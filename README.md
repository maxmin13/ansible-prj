# AWS Ansible project.

The project creates a datacenter in the AWS cloud.</br>
Python is used to create the the AWS objects (VPC, subnets, security groups, instances and DNS records),</br>
Ansible scripts to provision the instances.

**Requirements**:

- Fedora 34
- Python 3.11.2
- boto3 1.26.146
- botocore 1.29.146
- Jinja2 3.1.2
- moto 4.1.10
- pytest 7.3.1
- ansible 2.14.5

**Configure the AWS credentianls and default region on the controller machine**:

```
aws configure
```

**Create the AWS datacenter with instances, subnets, security groups and DNS records**.

```
cd bin
./make.sh

```

**Upgrade all the instances and istall some basic programs**:

```
cd provision
ansible-playbook -b -K playbooks/upgrade.yml
```

**Install Python 3.9.6 and create a virtual environment**: 

```
cd provision
ansible-playbook -b -K playbooks/python.yml
```

**Install nginx web server on all the instances tagged 'class:webserver':**

```
cd provision
ansible-playbook -b -K playbooks/nginx.yml
```

**Postgresql database instance and migration on all the instances tagged 'class:database'**:

```
cd provision
ansible-playbook -b -K playbooks/postgresql.yml
```


**Delete the AWS datacenter**:

```
cd bin
./delete.sh

```

<br>