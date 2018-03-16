import sys #handles low level functions of os

import operator #for arithmetic and comparision functions

import requests #for http requests

import json #for application of JSON

import twitter #twitter api

from watson_developer_cloud import PersonalityInsightsV2 as PersonalityInsights #Watson developer cloud

twitter_consumer_key = 'oiaTPbgrZnHyAvEUauEQqatk8'
twitter_consumer_secret = '0MkfT225mI4vVN2DYrvrPbXGeBThEbbHFR7NMrFmKBApbZ6KzR'
twitter_access_token = "850775446966939650-l6DVZIz9Ya79wDoOnvIuZUo7u81MxY3"
twitter_access_secret = 'XwDNplOJMo5zTRtoukhYjgX8dDuDlNTTG9UpgYT0iVjMZ'


twitter_api = twitter.Api(consumer_key = twitter_consumer_key, consumer_secret = twitter_consumer_secret,
                         access_token_key = twitter_access_token, access_token_secret = twitter_access_secret)

handle = ''
statuses = twitter_api.GetUserTimeline(screen_name = handle, count = 200, include_rts = False)

text = "" #tweets will be saved in this variable

for status in statuses:
  if(status.lang == 'en'): #English tweets
    text += status.text.encode('utf-8')
    
    
#The IBM Bluemix credentials for personality insights

pi_username = ''
pi_password = ''

personality_insights = PersonalityInsights( username = pi_username, password = pi_password)

def analyze(handle):
	pi_result = personality_insights.profile(text)
	return pi_result


def flatten(orig):
  data = {}
  for c in orig['tree']['children']:
    if 'children' in c:
      for c2 in c['chldren']:
        if 'children' in c2:
          for c3 in c2['children']:
            if 'children' in c3:
              for c4 in c3['children']:
                if(c4['category'] == 'personality'):
                  data[c4['id']] = c4['percentage']
                  if 'children' not in c3:
                    if (c3['category'] == 'personality'):
                                                data[c3['id']] = c3['percentage']
  return data
             
    
  def compare(dict1, dict2):
      compared_data={}
      for keys in dict1:
        if dict1[keys] != dict2[keys]:
          compared_data[keys] = abs(dict1[keys] - dict2[keys])
          
  return compared_data
                  
user_handle = "@MrKnowone"
celebrity_handle = "@iamsrk"

user_result = analyze(user_handle)
celebrity_result = analyze(celebrity_handle)

#flattening the results from the wason PI API
user = flatten(user_result)
celebrity = flatten(celebrity_result)

#comparing the results by calculating the distance b/w traits
compared_results = compare(user,celebrity)

sorted_result = sorted(compared_results.items(), key=operator.itemgetter(1))

for keys, value in sorted_result[:5]:
    print keys,
    print(user[keys]),
    print ('->'),
    print (celebrity[keys]),
    print ('->'),
    print (compared_results[keys])






