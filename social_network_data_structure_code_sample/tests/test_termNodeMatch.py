import unittest
from social_network_data_structure_code_sample.TermNodeMatch import *


class TestTermNodeMatch(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.matchFunctions = MatchingFunctions()
        cls.tweet_list = [
            {"text": "Via @ESPN https://t.co/WIW8SiIv9P", "node_id": "18908736", "message_id": "1116144023226540038",
             "message_time": "Thu Apr 11 01:00:46 +0000 2019"},
            {
                "text": "There's still time to get your tickets to the @BMTNofficial House Party! Hosted by myself and others",
                "node_id": "17008726", "message_id": "1115299026059124736",
                "message_time": "Mon Apr 08 17:03:03 +0000 2019"},
            {
                "text": ".@LilyCollins shows off the dramatic Les Miserables transformation that spooked her mom #FallonTonight https://t.co/dgixzfyqJp",
                "node_id": "19777398", "message_id": "1116190735336968192",
                "message_time": "Thu Apr 11 04:06:23 +0000 2019"},
            {"text": "Teens don\u2019t seem to grow out of problematic cell phone use https://t.co/WQu6dd2Bpn",
             "node_id": "125512325", "message_id": "1116077167102836736",
             "message_time": "Wed Apr 10 20:35:07 +0000 2019"},
            {
                "text": "Predators-Stars: Stanley Live updates from Game 1 of the Cup Playoffs first round https://t.co/v1V5ePQXIV",
                "node_id": "16639736", "message_id": "1116187882048368641",
                "message_time": "Thu Apr 11 03:55:03 +0000 2019"}
        ]
        cls.node_id_list = ['1115299026059124736', '125512325', '19777398', '1222']
        cls.tweet_json = [{tweet_json['message_id']: {"text": tweet_json['text'], "node_id": tweet_json['node_id']}} for
                          tweet_json in cls.tweet_list]
        cls.keyword_espn = {'@ESPN': [MatchingPhrase(message_id='1116144023226540038', node_id='18908736')]}
        cls.keyword_get_your_ticket = {
            'get your tickets': [MatchingPhrase(message_id='1115299026059124736', node_id='17008726')]}
        cls.keyword_les_miserables = {
            'les miserables': [MatchingPhrase(message_id='1116190735336968192', node_id='19777398')]}
        cls.keyword_cell = {
            'PROBLEMATIC CELL PHONE': [MatchingPhrase(message_id='1116077167102836736', node_id='125512325')]}
        cls.stanley_cup = {
            'stanley cup playoffs': [MatchingPhrase(message_id='1116187882048368641', node_id='16639736')]}

    def test_defaultDicForTweet(self):
        """
        This test checks whether a phrase should/shouldn't match a list of tweets.

        exactMatchPhraseInTweet -> exact phrase SHOULD match to a tweet containing this phrase from the list of tweets above.
        phraseLowerButTextCapital -> phrase is lower case and SHOULD match to a tweet containing this phrase but the phrase in
        the tweet has uppercase.
        phraseAllCapButTweetNot -> phrase is upper case and SHOULD match to a tweet containing this phrase but the phrase in
        the tweet is lowercase.
        subsetPhraseNotToInclude -> phrase SHOULD NOT match to a tweet containing this phrase BECAUSE of special character @, therefore
        not a match.
        phraseInTweetButOrderIncorrect -> phrase SHOULD NOT match to a tweet containing this phrase BECAUSE the phrase is
        out of order in the tweet

        """
        exactMatchPhraseInTweet = self.matchFunctions.checkPhraseInTweet(['get your tickets'], self.tweet_json)
        phraseLowerButTextCapital = self.matchFunctions.checkPhraseInTweet(['les miserables'], self.tweet_json)
        phraseAllCapButTweetNot = self.matchFunctions.checkPhraseInTweet(['PROBLEMATIC CELL PHONE'], self.tweet_json)
        subsetPhraseNotToInclude = self.matchFunctions.checkPhraseInTweet(['espn'], self.tweet_json)
        phraseInTweetButOrderIncorrect = self.matchFunctions.checkPhraseInTweet(['stanley cup playoffs'],
                                                                                self.tweet_json)

        self.assertEqual(exactMatchPhraseInTweet, self.keyword_get_your_ticket)
        self.assertEqual(phraseLowerButTextCapital, self.keyword_les_miserables)
        self.assertEqual(phraseAllCapButTweetNot, self.keyword_cell)
        self.assertNotEqual(subsetPhraseNotToInclude, self.keyword_espn)
        self.assertNotEqual(phraseInTweetButOrderIncorrect, self.stanley_cup)

    def test_matchNodeIdReturnTextMessageId(self):

        """
        This test checks whether the keyword dictionary's node_id matches to the list of node_id part of the setUp class above.

        nodeIdFromMatchNotInList -> This returns an empty list and should match accordingly
        nodeIdFromMatchInList -> SHOULD MATCH to the keyword with the node_id below


        """

        nodeIdFromMatchNotInList = list(
            self.matchFunctions.matchingNodeIdFromTweet(self.keyword_get_your_ticket, self.node_id_list))
        nodeIdFromMatchInList = list(self.matchFunctions.matchingNodeIdFromTweet(self.keyword_cell, self.node_id_list))

        self.assertEqual([], nodeIdFromMatchNotInList)
        self.assertEqual([[('PROBLEMATIC CELL PHONE', '1116077167102836736')]], nodeIdFromMatchInList)

    def test_isConsecutive(self):
        """
        This test is used to check whether a few numbers are consecutive or not.


        """
        consecutive_terms = [10, 11, 12]
        consecutive_even_terms = [0, 2, 4, 6, 8]
        random_list = [1, 0, 100, 2]
        self.assertEqual(True, self.matchFunctions.isConsecutive(consecutive_terms))
        self.assertEqual(False, self.matchFunctions.isConsecutive(consecutive_even_terms))
        self.assertEqual(False, self.matchFunctions.isConsecutive(random_list))


if __name__ == '__main__':
    unittest.main()
