import os
from azure.identity import ClientSecretCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.monitor import MonitorManagementClient
from itertools import groupby
from operator import itemgetter
from datetime import date, datetime, timedelta
from dotenv import load_dotenv
import alert


load_dotenv()

current_date = date.today()

Subscription_Id = os.getenv('SUBSCRIPTION_ID')

credential = ClientSecretCredential(
    tenant_id=os.getenv('TENANT_ID'),
    client_id=os.getenv('CLIENT_ID'),
    client_secret=os.getenv('CLIENT_SECRET'),
)


compute_client = ComputeManagementClient(credential, Subscription_Id)
resource_client = ResourceManagementClient(credential, Subscription_Id)
activity_client = MonitorManagementClient(credential, Subscription_Id)
revisit_resource = {}
current_date_formated = current_date.strftime("%d-%m-%Y")


def is_exist_vm(GROUP_NAME, RESOURCE_NAME):
    for vm in compute_client.virtual_machines.list(GROUP_NAME):
        if RESOURCE_NAME == vm.name:
            return True

def get_disk_count():
  count = 0
  for disk in compute_client.disks.list():
      if type(disk.managed_by) == type(None):
          count += 1
  return count


def list_vms_in_subscription():
    group_list = resource_client.resource_groups.list()
    for group in list(group_list):
        list_vms_in_groups(group.name)
    if len(revisit_resource) > 0:
        alert.send_revisit_alert(current_date_formated, revisit_resource, get_disk_count())  

def list_vms_in_groups(group_name):
    for resource in resource_client.resources.list_by_resource_group(group_name):
        #print(resource)
        if resource.type == "Microsoft.Compute/virtualMachines":
            vm_details = compute_client.virtual_machines.get(group_name, resource.name)
            if vm_details.tags is not None:
                if "revisit" in vm_details.tags:
                    currentDate = datetime.strptime(current_date_formated, "%d-%m-%Y")
                    revisitDate = datetime.strptime(vm_details.tags["revisit"], "%d-%m-%Y")
                    if currentDate >= revisitDate:
                        #print(vm_details.tags)
                        caller_id = None
                        if "CreatedBy" in vm_details.tags:
                            caller_id = vm_details.tags['CreatedBy']
                        if "createdBy" in vm_details.tags:
                            caller_id = vm_details.tags['createdBy']
                        if "createdby" in vm_details.tags:
                            caller_id = vm_details.tags['createdby']
                        if "Createdby" in vm_details.tags:
                            caller_id = vm_details.tags['Createdby']
                        alert_row = (
                            resource.id.lower().rsplit("/", 1)[-1]
                            + ", "
                            + vm_details.tags["revisit"]
                        )
                        if caller_id is not None:
                            #print(caller_id)
                            #print(alert_row);
                            if caller_id in revisit_resource.keys():
                                revisit_resource[caller_id].append(alert_row)
                            else:
                                revisit_resource[caller_id] = [alert_row]
        
    
                

            
list_vms_in_subscription()
#print(revisit_resource)
