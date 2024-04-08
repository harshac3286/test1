import os
from azure.identity import ClientSecretCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.resource import ResourceManagementClient
from itertools import groupby
from operator import itemgetter
from datetime import date, datetime, timedelta
from dotenv import load_dotenv
import alert
import upload_to_bucket
import botocore
import aws_connect as connect

aws_connect = connect.AwsConnect()

load_dotenv()

Subscription_Id = os.getenv("SUBSCRIPTION_ID")

credential = ClientSecretCredential(
    tenant_id=os.getenv("TENANT_ID"),
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
)


compute_client = ComputeManagementClient(credential, Subscription_Id)
resource_client = ResourceManagementClient(credential, Subscription_Id)


def get_disk_count():
    not_used_count = 0
    used_count = 0
    unused_disks = []
    for disk in compute_client.disks.list():
        if type(disk.managed_by) == type(None):
            not_used_count += 1
            unused_disks.append(disk.name)
        else:
            used_count += 1
    return [used_count, not_used_count, unused_disks]


def list_all_vm():
    running_count = 0
    stopped_count = 0
    for vm in compute_client.virtual_machines.list_all():
        array = vm.id.split("/")
        resource_group = array[4]
        vm_name = array[-1]
        statuses = compute_client.virtual_machines.instance_view(
            resource_group, vm_name
        ).statuses
        status = len(statuses) >= 2 and statuses[1]

        if status and status.code == "PowerState/running":
            running_count += 1

        if status and status.code == "PowerState/stopped":
            stopped_count += 1

    return [running_count, stopped_count]


def dic_to_report(cursor, title, data):
    cursor.write(f"{title} \n")
    cursor.write("-" * 80 + "\n")

    for key in data:
        cursor.write("%s\n" % (key))

    cursor.write("-" * 80 + "\n\n")


def generate_report():
    session = aws_connect.session_connect()
    current_date = date.today().strftime("%d-%m-%Y")
    get_disk_count_dict = get_disk_count()
    list_all_vm_dict = list_all_vm()
    path = "/home/ubuntu/automation-scripts/azure_resource_report"

    with open(path + "/report/report_" + current_date + ".txt", "w") as cursor:
        cursor.write("Total Running Instance : {} \n\n".format(list_all_vm_dict[0]))
        cursor.write("Total Stopped Instance : {} \n\n".format(list_all_vm_dict[1]))
        cursor.write("Total Volume in use : {} \n\n".format(get_disk_count_dict[0]))
        cursor.write("Total Volume NOT in use : {} \n\n".format(get_disk_count_dict[1]))

        dic_to_report(cursor, "Unused volume list", get_disk_count_dict[2])

    upload_to_bucket.upload_to_s3(session)

generate_report()
