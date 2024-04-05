import os
from google.cloud import compute_v1
from google.oauth2 import service_account

# Path to the service account key file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "<id>.json"

# Create a Compute Engine client
credentials = service_account.Credentials.from_service_account_file(os.environ["GOOGLE_APPLICATION_CREDENTIALS"])
client = compute_v1.InstancesClient(credentials=credentials)

# Define your project ID
project = '<id>'

request = compute_v1.AggregatedListInstancesRequest()
request.project = project
# Use the `max_results` parameter to limit the number of results that the API returns per response page.
request.max_results = 50

agg_list = client.aggregated_list(request=request)

print("Instances found:")
for zone, response in agg_list:
    if response.instances:
        for instance in response.instances:
            print(f" - {instance.labels}")
