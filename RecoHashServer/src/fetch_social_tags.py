import requests
import json
import oauth2 as oauth

def insta_hashtags(tag):
	insta_access_token = #INSTA TOKEN
	insta_api_url = 'https://api.instagram.com/v1/tags/search?q='+tag+'&access_token='+insta_access_token
	r = requests.get(insta_api_url).json()
	tweet_and_count = {}
	for i in r['data']:
		new_dict_key = str(i.get('name').encode('ascii','ignore').decode('utf-8')).lower()#.encode('ascii','ignore')).lower()
		new_dict_val = i.get('media_count')
		tweet_and_count[new_dict_key] = new_dict_val
	return tweet_and_count



def tweet_hashtags(tag, insta_tags):
	twitter_api_key = #TWITTER KEY
	twitter_api_secret = #TWITTER_API_SECRET
	consumer = oauth.Consumer(key=twitter_api_key, 
		secret=twitter_api_secret)
	request_token_url = "https://api.twitter.com/1.1/search/tweets.json?q=%23" + tag +"&count=10000&result_type=mixed"
	client = oauth.Client(consumer)
	# The OAuth Client request works just like httplib2 for the most part.
	resp, content = client.request(request_token_url ,"GET")
	jsonResponse = json.loads(content.decode('utf-8'))
	taglist = []
	for status in jsonResponse['statuses']:
		for hashtag in status['entities']['hashtags']:
			twitter_dict_key = str(hashtag['text'].encode('ascii','ignore').decode('utf-8')).lower()
			if insta_tags.get(twitter_dict_key)!=None and twitter_dict_key not in taglist:
				taglist.append(twitter_dict_key)
	return taglist

