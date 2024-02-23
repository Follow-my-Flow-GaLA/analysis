import requests

URL = "http://localhost:5000/api/danger_zone/phase1?confirm_delete=Confirm%20Delete%20Phase1"

# ask for confirmation
print('Type "Confirm_Delete_Phase1" to confirm the deletion')
confirm_msg = raw_input('Type here: ')
if confirm_msg == "Confirm_Delete_Phase1":
    response = requests.delete(URL)
    if response.status_code == 200:
        print("All data from phase1 has been deleted")
    else:
        print("Error during deletion")
else:
    print("Deletion not confirmed")