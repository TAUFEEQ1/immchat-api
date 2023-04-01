import json
import re
regex = re.compile(r"\b(please|kindly|inbox|DM|dm|Please)\b")
with open("twitter_qa.json",'r') as f:
    data = f.read()
    
twitter_db = json.loads(data)

clean_db = []
for tweet in twitter_db:
    if regex.search(tweet['ans']):
        continue
    elif len(tweet['ans'])< 70:
        continue
    else:
        clean_db.append(tweet)

print(len(clean_db))
with open("clean_tweets.json","w") as f:
    json.dump(clean_db,f)
