import requests
import json
import oauth2 as oauth


input_name = input('Enter input: ')
insta_access_token = '1649756197.244359a.dabb5f7dad544aef808365883b1c0f17'
twitter_api_key = 'yxs4iq4N37bAz61fxemDyk9bY'
twitter_api_secret = 'mviDIA309YCEIUTJlZatl5P09LgWlOMK1ZJVcZBlg9v2t3vgPN'
insta_api_url = 'https://api.instagram.com/v1/tags/search?q='+input_name+'&access_token='+insta_access_token
print(insta_api_url)

r = requests.get(insta_api_url).json()
tweet_and_count = {}
for i in r['data']:
	new_dict_key = str(i.get('name').encode('ascii','ignore')).lower()
	new_dict_val = i.get('media_count')
	tweet_and_count[new_dict_key] = new_dict_val

for k,v in tweet_and_count.items():
	print('Key: '+k+' Value: '+str(v))

consumer = oauth.Consumer(key=twitter_api_key, 
    secret=twitter_api_secret)
request_token_url = "https://api.twitter.com/1.1/search/tweets.json?q=%23" + input_name +"&count=100000&result_type=mixed"
# request_url_recent = ''
# request_url_popular = '&result_type=popular'

# Create our client.
client = oauth.Client(consumer)

# The OAuth Client request works just like httplib2 for the most part.
resp, content = client.request(request_token_url ,"GET")
jsonResponse = json.loads(content.decode('utf-8'))
taglist = []
for status in jsonResponse['statuses']:
	for hashtag in status['entities']['hashtags']:
		twitter_dict_key = str(hashtag['text'].encode('ascii','ignore')).lower()
		if tweet_and_count.get(twitter_dict_key)!=None and twitter_dict_key not in taglist:
			taglist.append(twitter_dict_key)
		# else:
		# 	tweet_and_count[twitter_dict_key] += 1
for retrieved_tag in taglist:
	print(retrieved_tag)
# print("============================NEW DICTIONARY===============================")
# for k,v in tweet_and_count.items():
# 	print('Key: '+k+' Value: '+str(v))

