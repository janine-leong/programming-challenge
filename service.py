import requests
import time
import json
from shapely.geometry import shape, Point



api_url = "https://3qbqr98twd.execute-api.us-west-2.amazonaws.com/test"
email_address = "sprinter-eng-test@guerrillamail.info"

# GET from api (api_url) to get clinician status data for clinician #clinicianID
def get_clinician_status(clinicianID):
  url = f"{api_url}/clinicianstatus/{clinicianID}"
  response = requests.get(url)
  if response.status_code == 200:
    data = response.json()
    return data
  else:
    print("Alert! Endpoint did not return: {response.status_code}")
  print(response)

# check if clinician is in safe zone
def in_zone(clinician_status):
  

# send email to email_address with missing phlebotomist’s ID
def send_email(email_address):


def main():
  testIDs = [1,2,3,4,5,6,7]

  while True:
    for i in range(len(testIDs)):
      print(f"clinician {testIDs[i]} status:")
      clinician_status = get_clinician_status(testIDs[i])
      print(json.dumps(clinician_status, indent=4))
    time.sleep(10)

if __name__ == "__main__":
    main()