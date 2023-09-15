import simple
from clarifai.client.user import User
PAT = simple.model.api_key
USER_ID = simple.model.user_id
APP_ID = simple.model.app_id
client = User(user_id=USER_ID)
#print(client)
import json
ap = client.list_apps()
for a in ap:
    wf = a .list_workflows()
    #print(a,.sjoinwf)
    for w in wf:
        #print({"a":str(a),
        #"w":str(w)})
        print(w.id)
        #print(json.dumps(w2))
