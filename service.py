import requests
import time
import json
from shapely.geometry import shape, Point
import smtplib
from email.message import EmailMessage

api_url = "https://3qbqr98twd.execute-api.us-west-2.amazonaws.com/test"
recipient_email = "sprinter-eng-test@guerrillamail.info"
# recipient_email = "coding-challenges+alerts@sprinterhealth.com"
sender_email = "testemailforjl@gmail.com"
password = "nclpoyahimpfabsd"

# GET from api (api_url) to get clinician status data for clinician #clinicianID
def get_clinician_status(clinicianID):
  try:
    url = f"{api_url}/clinicianstatus/{clinicianID}"
    response = requests.get(url)
    response.raise_for_status() 
    data = response.json()
    return data
  except Exception as e:
    print(f"Alert! Endpoint did not return: {e}")
    return None

# check if clinician is in safe zone
def in_zone(clinician_status):
  point = None
  for feature in clinician_status['features']:
    if feature["geometry"]["type"]=="Point": 
      x,y = feature['geometry']['coordinates']
      point = Point(x,y)
      break
  for feature in clinician_status['features']:
    if feature["geometry"]["type"]=="Polygon": 
      polygon = shape(feature['geometry'])
      if polygon.intersects(point):
        return True
  return False
  

# send email to email_address with missing phlebotomist’s ID
def send_email(sender_email, recipient_email, body):
  try:
    textfile = "email.txt"
    with open(textfile, "w") as f:
      f.write(body)
    with open(textfile) as fp:
      msg = EmailMessage()
      msg.set_content(fp.read())
    msg['Subject'] = "Alert - missing clinician"
    msg['From'] = sender_email
    msg['To'] = recipient_email
    with smtplib.SMTP('smtp.gmail.com', 587) as s:
      s.starttls()
      s.login(sender_email, password)
      s.send_message(msg)
  except Exception as e:
    print(f"send_email exception: {e}")


def main():
  clinicianIDs = [1,2,3,4,5,6]
  for j in range(30):
    for i in range(len(clinicianIDs)):
      print(f"clinician {clinicianIDs[i]} status:")
      clinician_status = get_clinician_status(clinicianIDs[i])
      if clinician_status and clinician_status.get('features'):
        print(json.dumps(clinician_status, indent=2))
        print(f"in zone? {in_zone(clinician_status)}")
        if not in_zone(clinician_status):
          send_email(sender_email, recipient_email, f"Clinician {clinicianIDs[i]} is missing")
    time.sleep(60)

if __name__ == "__main__":
  main()