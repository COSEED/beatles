import urlparse
import oauth2 as oauth
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import time

username=""
password=""

consumer_key = '' #belongs to app
consumer_secret = ''

request_token_url = 'https://api.twitter.com/oauth/request_token'
access_token_url = 'https://api.twitter.com/oauth/access_token'
authorize_url = 'https://api.twitter.com/oauth/authorize'

consumer = oauth.Consumer(consumer_key, consumer_secret)
client = oauth.Client(consumer)

# Step 1: Get a request token. This is a temporary token that is used for
# having the user authorize an access token and to sign the request to obtain
# said access token.

resp, content = client.request(request_token_url, "GET")
if resp['status'] != '200':
    raise Exception("Invalid response %s." % resp['status'])

request_token = dict(urlparse.parse_qsl(content))

print "Request Token:"
print "    - oauth_token        = %s" % request_token['oauth_token']
print "    - oauth_token_secret = %s" % request_token['oauth_token_secret']
print

# Step 2: Redirect to the provider. Since this is a CLI script we do not
# redirect. In a web application you would redirect the user to the URL
# below.

print "Go to the following link in your browser:"
print "%s?oauth_token=%s" % (authorize_url, request_token['oauth_token'])
print


#step 3 open link in browser

fullUrl =  "%s?oauth_token=%s" % (authorize_url, request_token['oauth_token'])
driver = webdriver.Chrome()
driver.maximize_window()
driver.implicitly_wait(5)
driver.get(fullUrl)

userLoginInput = driver.find_element_by_id("username_or_email")

userLoginInput.send_keys(username)

time.sleep(5)



passwordInput = driver.find_element_by_id("password")
passwordInput.send_keys(password)

time.sleep(5)

authorizeButton = driver.find_element_by_class_name("submit")
authorizeButton.click()

time.sleep(5)

pinTag = driver.find_element_by_tag_name("code")

pin = pinTag.text;

print pin
# After the user has granted access to you, the consumer, the provider will
# redirect you to whatever URL you have told them to redirect to. You can
# usually define this in the oauth_callback argument as well.
#accepted = 'n'
#while accepted.lower() == 'n':
#    accepted = raw_input('Have you authorized me? (y/n) ')
#oauth_verifier = raw_input('What is the PIN? ')

time.sleep(5)

driver.quit();

oauth_verifier = pin

# Step 3: Once the consumer has redirected the user back to the oauth_callback
# URL you can request the access token the user has approved. You use the
# request token to sign this request. After this is done you throw away the
# request token and use the access token returned. You should store this
# access token somewhere safe, like a database, for future use.
token = oauth.Token(request_token['oauth_token'],
    request_token['oauth_token_secret'])
token.set_verifier(oauth_verifier)
client = oauth.Client(consumer, token)

resp, content = client.request(access_token_url, "POST")
access_token = dict(urlparse.parse_qsl(content))

print "Access Token:"
print "    - oauth_token        = %s" % access_token['oauth_token']
print "    - oauth_token_secret = %s" % access_token['oauth_token_secret']
print
print "You may now access protected resources using the access tokens above."
print