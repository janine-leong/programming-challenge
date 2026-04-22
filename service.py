import requests
import json


base_url = "https://3qbqr98twd.execute-api.us-west-2.amazonaws.com/test"

def get_clinician_status(clinicianID):
  url = f"{base_url}/clinicianstatus/{clinicianID}"
  response = requests.get(url)
  if response.status_code == 200:
    data = response.json()
    return data
  else:
    print("alert: failed to get clinician status {response.status_code}")
  print(response)

testID = 7
clinician_status = get_clinician_status(testID)
print(json.dumps(clinician_status, indent=4))

# if clinician_status:
#   print(f"{clinician_status}")