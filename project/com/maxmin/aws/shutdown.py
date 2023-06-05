import sys

from com.maxmin.aws.configuration import ApplicationConfig
from com.maxmin.aws.constants import ProjectFiles, Route53Constants
from com.maxmin.aws.ec2.dao import internet_gateway
from com.maxmin.aws.ec2.dao.image import Image
from com.maxmin.aws.ec2.dao.instance import Instance
from com.maxmin.aws.ec2.dao.internet_gateway import InternetGateway
from com.maxmin.aws.ec2.dao.route_table import RouteTable
from com.maxmin.aws.ec2.dao.security_group import SecurityGroup
from com.maxmin.aws.ec2.dao.ssh import Keypair
from com.maxmin.aws.ec2.dao.subnet import Subnet
from com.maxmin.aws.ec2.dao.vpc import Vpc
from com.maxmin.aws.logs import Logger
from com.maxmin.aws.route53.dao.hosted_zone import HostedZone
from com.maxmin.aws.route53.dao.record import Record

if __name__ == "__main__":
    if len(sys.argv) < 2:
        application_config = ApplicationConfig(
            ProjectFiles.DEFAULT_CONFIG_FILE
        )
    else:
        application_config = ApplicationConfig(sys.argv[1])

    Logger.info("Deleting datacenter ...")

    vpc = Vpc(application_config.vpc.name)
    vpc_found = vpc.load()

    if vpc_found is False:
        Logger.warn("Vpc not found!")

    #
    # Delete the instances
    #

    route53Constants = Route53Constants()
    hosted_zone = HostedZone(route53Constants.registered_domain)
    hosted_zone.load()

    for instance_config in application_config.instances:
        instance = Instance(instance_config.tags)

        found_instance = instance.load()
        record = Record(instance_config.dns_name, hosted_zone.id)

        if record.load() is True:
            record.delete(instance.public_ip)

            Logger.info("DNS record successfully deleted!")
        else:
            Logger.warn("DNS record already deleted!")

        if found_instance is True and instance.state != "terminated":
            Logger.info("Deleting instance ...")

            instance.delete()

            Logger.info("Instance deleted!")

        else:
            Logger.warn("Instance already deleted!")

        keypair = Keypair(instance_config.keypair)

        if keypair.load() is True:
            keypair.delete()

        # delete the corresponding AMI
        if instance_config.target_img is not None:
            target_image = Image(instance_config.target_img)

            if target_image.load() is True:
                Logger.info("Deleting target image ...")

                target_image.delete()

                Logger.info("Target image deleted!")
            else:
                Logger.warn("Target image not found!")

    #
    # Delete the security groups
    #

    for security_group_config in application_config.security_groups:
        security_group = SecurityGroup(security_group_config.name)

        if security_group.load() is True:
            security_group.delete()

            Logger.info("Security group deleted!")
        else:
            Logger.warn("Security group already deleted!")

    #
    # Delete the internet gateway
    #

    internet_gateway = InternetGateway(application_config.internet_gateway)

    if internet_gateway.load() is True:
        if internet_gateway.is_attached_to(vpc.id):
            internet_gateway.detach_from(vpc.id)

        internet_gateway.delete()

        Logger.info("Internet gateway deleted!")
    else:
        Logger.warn("internet gateway already deleted!")

    #
    # Delete the subnets
    #

    for subnet_config in application_config.subnets:
        subnet = Subnet(subnet_config.name)

        if subnet.load() is True:
            subnet.delete()

            Logger.info("Subnet deleted!")
        else:
            Logger.warn("subnet already deleted!")

    #
    # Delete the route table
    #

    route_table = RouteTable(application_config.route_table)

    if route_table.load() is True:
        route_table.delete()

        Logger.info("Route table deleted!")
    else:
        Logger.warn("route table already deleted!")

    #
    # Delete the vpc
    #

    vpc = Vpc(application_config.vpc.name)
    vpc_found = vpc.load()

    if vpc_found is True:
        vpc.delete()

        Logger.info("Vpc delete!")
    else:
        Logger.warn("vpc already deleted!")

    Logger.info("Datacenter deleted!")
