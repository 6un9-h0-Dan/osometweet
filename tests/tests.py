import sys
import os
import unittest
import osometweet

api_key = os.environ.get('API_KEY', '')
api_key_secret = os.environ.get('API_KEY_SECRET', '')
access_token = os.environ.get('ACCESS_TOKEN', '')
access_token_secret = os.environ.get('ACCESS_TOKEN_SECRET', '')
bearer_token = os.environ.get("BEARER_TOKEN")

class TestOauth(unittest.TestCase):
    """
    Make sure the oauth is working
    """
    def test_1a(self):
        oauth1a = osometweet.OAuth1a(
            api_key=api_key,
            api_key_secret=api_key_secret,
            access_token=access_token,
            access_token_secret=access_token_secret
        )
        test_tweet_id = '1323314485705297926'
        resp = oauth1a.make_request(
            'https://api.twitter.com/2/tweets',
            {"ids": f"{test_tweet_id}"}
            ).json()
        self.assertEqual(resp['data'][0]['id'], test_tweet_id)
    
    def test_1a_exception(self):
        with self.assertRaises(ValueError):
            osometweet.OAuth1a(api_key=1)
        with self.assertRaises(ValueError):
            osometweet.OAuth1a(api_key_secret=1)
        with self.assertRaises(ValueError):
            osometweet.OAuth1a(access_token=1)
        with self.assertRaises(ValueError):
            osometweet.OAuth1a(access_token_secret=1)
    
    def test_2(self):
        oauth2 = osometweet.OAuth2(bearer_token=bearer_token)
        test_tweet_id = '1323314485705297926'
        resp = oauth2.make_request(
            'https://api.twitter.com/2/tweets',
            {"ids": f"{test_tweet_id}"}
            ).json()
        self.assertEqual(resp['data'][0]['id'], test_tweet_id)
    
    def test_2_exception(self):
        with self.assertRaises(ValueError):
            osometweet.OAuth2(bearer_token=1)

class TestAPI(unittest.TestCase):
    """
    Test all the API endpoints
    """
    def setUp(self):
        oauth2 = osometweet.OAuth2(bearer_token=bearer_token)
        self.ot = osometweet.OsomeTweet(oauth2)

    def test_tweet_lookup(self):
        test_tweet_ids = ['1323314485705297926', '1328838299419627525']
        resp = self.ot.tweet_lookup(tids=test_tweet_ids)
        for tweet in resp['data']:
            self.assertIn(tweet['id'], test_tweet_ids) 
    
    def test_user_lookup_ids(self):
        test_user_ids = ['12', '13']
        resp = self.ot.user_lookup_ids(test_user_ids)
        for user in resp['data']:
            self.assertIn(user['id'], test_user_ids) 

    def test_user_lookup_usernames(self):
        test_user_usernames = ['jack', 'biz']
        resp = self.ot.user_lookup_usernames(test_user_usernames)
        for user in resp['data']:
            self.assertIn(user['username'], test_user_usernames) 

class TestUtils(unittest.TestCase):
    """
    Test all the utils endpoints
    """

    ### Two tests for the chunker method ###
    def test_chunker(self):
        test_list = [1,2,3,4,5,6,7,8,9]
        chunk_sizes = [2,3]
        correct_responses = [
        [[1, 2], [3, 4], [5, 6], [7, 8],
        [9]],[[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        ]
        zipper = zip(chunk_sizes, correct_responses)
        for chunk_size, correct_resp in zipper:
            resp = osometweet.utils.chunker(
                seq = test_list,
                size = chunk_size
                )
            self.assertEqual(resp, correct_resp)

    ### Test return object fields methods ###
    def test_rt_user_fields(self):
        """Test return user fields method"""
        correct_fields = [
            "created_at",
            "description",
            "entities",
            "id",
            "location",
            "name",
            "pinned_tweet_id",
            "profile_image_url",
            "protected",
            "public_metrics",
            "url",
            "username",
            "verified",
            "withheld"
        ]
        fields = osometweet.utils.ObjectFields.return_user_fields()
        self.assertEqual(fields, correct_fields)

    def test_rt_tweet_fields(self):
        """Test return tweet fields method"""
        correct_fields = [
            "attachments",
            "author_id",
            "context_annotations",
            "conversation_id",
            "created_at",
            "entities",
            "geo",
            "id",
            "in_reply_to_user_id",
            "lang",
            "non_public_metrics",
            "organic_metrics",
            "possiby_sensitive",
            "promoted_metrics",
            "public_metrics",
            "referenced_tweets",
            "reply_settings",
            "source",
            "text",
            "withheld"
        ]
        response = osometweet.utils.ObjectFields.return_tweet_fields()
        self.assertEqual(response, correct_fields)

    def test_rt_media_fields(self):
        """Test return media fields method"""
        correct_fields = [
            "duration_ms",
            "height",
            "media_key",
            "non_public_metrics",
            "organic_metrics",
            "preview_image_url",
            "promoted_metrics",
            "public_metrics",
            "type",
            "width"
        ]
        response = osometweet.utils.ObjectFields.return_media_fields()
        self.assertEqual(response, correct_fields)

    def test_rt_poll_fields(self):
        """Test return poll fields method"""
        correct_fields = [
            "duration_minutes",
            "end_datetime",
            "id",
            "options",
            "voting_status"
        ]
        response = osometweet.utils.ObjectFields.return_poll_fields()
        self.assertEqual(response, correct_fields)

    def test_rt_place_fields(self):
        """Test return place fields method"""
        correct_fields = [
            "contained_within",
            "country",
            "country_code",
            "full_name",
            "geo",
            "id",
            "name",
            "place_type",
        ]
        response = osometweet.utils.ObjectFields.return_place_fields()
        self.assertEqual(response, correct_fields)

if __name__ == "__main__":
    unittest.main()