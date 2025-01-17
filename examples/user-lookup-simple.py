#!/usr/bin/env python3

# Script Information
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
Purpose: 
    A simple example script for pulling user account information 
    with the handy osometweet package. It is meant to show you 
    how to use the method, but also how it is working. 

Author: Matthew DeVerna
Date: Dec. 17th 2020
"""


# First things first, import the necessary packages
import os
from osometweet.api import OsomeTweet

# Now we can initialize an object w. the of the OsomeTweet class
ot = OsomeTweet()


"""
Now with this object `ot` you have access to a number of
different helpful methods for getting Twitter data. 

This script will show you how to use the .user_lookup_ids()
method.

The second thing we need to do is set our 
user tokens to get Oauth_1.0a authortization.

#### Access your keys/tokens ###
To find your access tokens/keys, you can visit the below
site. 
  - https://developer.twitter.com/en/portal/projects-and-apps

Once there click "Edit" next to "App Permisions." 
Next, select "Keys and Tokens." What you're looking for 
is under "Access token & secret." You can regenerate these
if you have forgotten them, however, keep in mind this will
change your access keys/tokens and may break other code
that relied on those tokens/keys.
"""

# To set your enviornment variables, in your terminal execute
# a command like:
#       export 'CONSUMER_KEY'='<your_consumer_token>'
# replacinging <your_consumer_token> with the tokens that 
# Twitter provided you. Repeat this process for each token 
# that you need. This set's environment variables that you
# can load using the `os.environ.get()` method as you see
# below.

# Set Twitter tokens/keys.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
api_key = os.environ.get("TWITTER_API_KEY")
api_key_secret = os.environ.get("TWITTER_API_KEY_SECRET")
access_token = os.environ.get("TWITTER_ACCESS_TOKEN")
access_token_secret = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")

# With these keys/tokens, we can initialize the OsomeTweet
# object (ot)
ot = OsomeTweet(
    api_key = api_key,
    api_key_secret = api_key_secret,
    access_token = access_token,
    access_token_secret = access_token_secret
    )

"""
Now we can use the .user_lookup_ids() method to pull data.

This method utilizes the keys/tokens provided and takes in
a list (or tuple) of user ids (100 user_ids max), and a 
list (or tuple) of user_fields (from those available).

The method defaults to including the user_fields below...
    - id, name, username
... because these are the default fields set by Twitter when
calling the endpoint without passing any user_fields.

Here's what it looks like in use...
"""

# Set some test IDs (these are Twitter's own accounts)
ids2find = ["2244994945", "6253282"]

# Call the function without any additional user_fields
response = ot.user_lookup_ids(
                user_ids=ids2find
                )

# To call the function with different user_fields
# comment out the above code and uncomment the
# code below, then run the script again and 
# take a look at the new fields returned.

# new_user_fields = [
#     "created_at", "description",
#     "entities", "public_metrics"
# ]
# response = ot.user_lookup_ids(
#                 user_ids=ids2find,
#                 user_fields=new_user_fields
#                 )

# The .user_lookup_ids() method utilizes the response
# package to communicate with twitter, and it returns a
# the response.json() object. We find the data object 
# by calling...
data = response["data"]

# The data object above is a list of dictionaries. Thus,
# we can iterate through the data returned for each user
# by doing the below.

for user in data:
    print(user)

"""
To gather data from specific fields (e.g. the `id` 
number) within the for loop you can access it by
calling user.get("id") or user["id"]

Finally, wou will also get errors for users which 
can't be found by calling using the response object
with:
    errors = response.json()['errors']
this is not used here because the Twitter accounts
will never return errors. If this is the case, the
errors object will simply become a None type object.

"""