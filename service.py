import requests
import time
import json
from shapely.geometry import shape, Point
import smtplib, ssl
from email.message import EmailMessage

api_url = "https://3qbqr98twd.execute-api.us-west-2.amazonaws.com/test"
recipient_email = "sprinter-eng-test@guerrillamail.info"
sender_email = "testemailforjl@gmail.com"
password = "nclpoyahimpfabsd"

# GET from api (api_url) to get clinician status data for clinician #clinicianID
def get_clinician_status(clinicianID):
  url = f"{api_url}/clinicianstatus/{clinicianID}"
  response = requests.get(url)
  if response.status_code == 200:
    data = response.json()
    return data
  else:
    print("Alert! Endpoint did not return: {response.status_code}")

# check if clinician is in safe zone
def in_zone(clinician_status):
  x,y = clinician_status['features'][0]['geometry']['coordinates']
  point = Point(x,y)
  # print(f"point {point}")

  for feature in clinician_status['features']:
    if feature["geometry"]["type"]=="Polygon": 
      polygon = shape(feature['geometry'])
      # print(polygon)
      if polygon.intersects(point):
        return True
  return False
  

# send email to email_address with missing phlebotomist’s ID
def send_email(sender_email, recipient_email, body):
  print(f"sender address: {sender_email}\nreceiving address: {recipient_email}\nbody: {body}")
  textfile = "email.txt"
    
  with open(textfile, "w") as f:
    f.write(body)
  with open(textfile) as fp:
    msg = EmailMessage()
    msg.set_content(fp.read())

  msg['Subject'] = f'alert'
  msg['From'] = sender_email
  msg['To'] = recipient_email

  with smtplib.SMTP('smtp.gmail.com', 587) as s:
    s.starttls()
    s.login(sender_email, password)
    s.send_message(msg)


def main():
  clinicianIDs = [1,2,3,4,5,6]
  while True:
    for i in range(len(clinicianIDs)):
      print(f"clinician {clinicianIDs[i]} status:")
      clinician_status = get_clinician_status(clinicianIDs[i])
      print(f"in zone? {in_zone(clinician_status)}")
      if not in_zone(clinician_status):
        send_email(sender_email, recipient_email, f"missing clinician: {clinicianIDs[i]}")
      print(json.dumps(clinician_status, indent=2))
    time.sleep(10)
  # send_email(sender_email, recipient_email, "test email")

if __name__ == "__main__":
  main()