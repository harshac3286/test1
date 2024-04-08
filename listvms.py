from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.resource import ResourceManagementClient
from azure.identity import ClientSecretCredential
from tabulate import tabulate
import requests
from dotenv import load_dotenv
import os

load_dotenv()
subscription_id = os.getenv('SUBSCRIPTION_ID')

credential = ClientSecretCredential(
    tenant_id=os.getenv('TENANT_ID'),
    client_id=os.getenv('CLIENT_ID'),
    client_secret=os.getenv('CLIENT_SECRET'),
)

webhook_url = os.getenv('WEBHOOK_URL')

def list_vm_info_across_resource_groups():
    compute_client = ComputeManagementClient(credential, subscription_id)
    resource_client = ResourceManagementClient(credential, subscription_id)

    # Get all resource groups in the subscription
    resource_groups = resource_client.resource_groups.list()

    # Create a list to store table data
    table_data = []

    # Add rows to the table data
    for resource_group in resource_groups:
        vms = compute_client.virtual_machines.list(resource_group.name)

        for vm in vms:
            tags = vm.tags or {}
            created_by_value = tags.get("CreatedBy", "Tag not found")
            revisit_date = tags.get("revisit", "Tag not found")
            schedule = tags.get("Schedule", "Tag not found")
            table_data.append([vm.name, vm.hardware_profile.vm_size, revisit_date, created_by_value, schedule])

    # Convert the table data to a formatted table string with a header
    table_str = f'List of VMs in Dev/Test Subscription:\n\n{tabulate(table_data, headers=["VM Name", "VM Size", "Revisit Date", "CreatedBy", "Schedule"], tablefmt="simple")}'

    # Send the table to Google Chat using webhook URL
    send_to_google_chat(table_str)

def send_to_google_chat(message):
    # Send the message to Google Chat using webhook URL
    payload = {'text': f'```\n{message}\n```'}
    response = requests.post(webhook_url, json=payload)

    if response.status_code == 200:
        print('Message sent to Google Chat.')
    else:
        print(f'Failed to send message. Status code: {response.status_code}, Response content: {response.content}')

if __name__ == "__main__":
    list_vm_info_across_resource_groups()
