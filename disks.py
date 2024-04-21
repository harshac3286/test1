import subprocess
import json

def list_gcp_disks(project_id):
    try:
        # Run the gcloud command to list disks
        cmd = f"gcloud compute disks list --project {project_id} --format=json"
        output = subprocess.check_output(cmd, shell=True)

        # Parse the output as JSON
        disks = json.loads(output)

        # Print the disk information
        for disk in disks:
            print("Disk name:", disk["name"])
            print("Disk size (GB):", disk["sizeGb"])
            print("Disk type:", disk["type"])
            print("Zone:", disk["zone"])
            print("-------------------------------------------------------")

    except Exception as e:
        print("An error occurred:", e)

# Replace 'your-project-id' with your actual GCP project ID
project_id = ''

# Call the function to list disks
list_gcp_disks(project_id)
