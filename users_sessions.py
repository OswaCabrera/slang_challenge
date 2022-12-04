import requests
from datetime import datetime
import json 

def get_seconds(string_date_finish, string_date_start):
    date_format1 = string_date_finish[:10] + ' ' + string_date_finish[12:19]
    date_format2 = string_date_start[:10] + ' ' + string_date_start[12:19]
    date1 = datetime.strptime(date_format1, '%Y-%m-%d %H:%M:%S')
    date2 = datetime.strptime(date_format2, '%Y-%m-%d %H:%M:%S')
    diff = (date1-date2)
    # print( diff.seconds )
    return diff.seconds


def build_user_sessions(activities_json):
    # Dictionary
    activities_array = activities_json['activities']
    users_sessions = {}
    for activities in activities_array:
        if (activities["user_id"] in users_sessions):
            aux = users_sessions[activities['user_id']]
            if ( get_seconds(activities["answered_at"] , aux[-1]["ended_at"]) < 300 ) :
                aux[-1]["ended_at"] = activities['answered_at']
                aux[-1]["activity_ids"].append(activities["id"])
                aux[-1]["duration_seconds"] = get_seconds(activities["answered_at"], aux[-1]["started_at"])
            else:
                aux.append({ "ended_at" : activities["answered_at"], "started_at" : activities["first_seen_at"], "activity_ids" : [activities["id"]], "duration_seconds": get_seconds(activities["answered_at"] , activities["first_seen_at"]) })
            users_sessions[activities['user_id']] = aux
        else:
            users_sessions[activities['user_id']] = [ {"ended_at" : activities["answered_at"], "started_at" : activities["first_seen_at"], "activity_ids" : [activities["id"]], "duration_seconds": get_seconds(activities["answered_at"] , activities["first_seen_at"])  } ]
      
    return users_sessions

def main():

    user_sessions = {}
    activities_response = requests.get("https://api.slangapp.com/challenges/v1/activities",headers={"Authorization": "Basic MTQ0Om5aRUlBYkgvaFFFR2RNRnVDYnpOZlU2cmt2eUEyclVWWmpNeTZaRVFMQTQ9"}) # ← replace with your key
    
    if activities_response.status_code == requests.codes.ok:
        # Succes (Code 200)
        user_sessions = {"user_sessions": build_user_sessions(activities_response.json())}
    else:
        #Fail
        return -1
    
    print(json.dumps(user_sessions, indent=3))

    requests.post("https://api.slangapp.com/challenges/v1/activities/sessions",
    headers={"Authorization": "Basic MTQ0Om5aRUlBYkgvaFFFR2RNRnVDYnpOZlU2cmt2eUEyclVWWmpNeTZaRVFMQTQ9"}, 
    json=user_sessions) # Keep in mind this should be a dictionary {“user_sessions”: {...}}

if __name__ == "__main__":
    main()