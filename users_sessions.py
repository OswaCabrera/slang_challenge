import requests
activities_response = requests.get("https://api.slangapp.com/challenges/v1/activities",headers={"Authorization": "Basic MTXsh9S...=="}) # ← replace with your key
# activities_response.json() now gives you a python array of activities. You can now start
# iterating this array so you can start grouping by user sessions as per the spec.
# How would you implement this? This is the core of the challenge!
user_sessions = {"user_sessions": build_user_sessions(activities_response.json())}

# Once you have that ready you can post it with:
requests.post("https://api.slangapp.com/challenges/v1/activities/sessions",
headers={"Authorization": "Basic MT...=="}, # ← replace with your key
json=user_sessions) # Keep in mind this should be a dictionary {“user_sessions”: {...}}