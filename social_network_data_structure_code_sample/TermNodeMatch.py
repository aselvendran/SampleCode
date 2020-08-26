from matchingFunctions import *
import json


class TweetMessageNodeMapping:
    """
    Data Processing Class
    """

    def __init__(self, tweetsFileName, termFileName, nodeFile, fileToSave):
        self.tweetsFileName = tweetsFileName
        self.termFileName = termFileName
        self.nodeFile = nodeFile
        self.fileToSave = fileToSave
        self.matchingFunctions = MatchingFunctions()

    def readFileInChunk(self, file, chunkSize=5000):

        """
        Read data in Chucks and returning generator.

        :param file: file to open
        :param chunkSize: size to read default 5000
        :return: generator of the data
        """
        while True:
            text_data = file.read(chunkSize)
            if not text_data:
                break
            yield text_data

    # TODO PART OF THE KINSIS LIsTENER
    def readTweets(self, termsData):

        """
        With the terms data pass as variable; this function will read the tweets data (file name initialized in class)
        and match the terms that appear in the tweet data.

        :param termsData: the terms data as a string.
        :return: generator that yields only the terms that match tweets.
        """
        file = open('%s.jsonl' % self.tweetsFileName)
        for json_ in file:
            tweet_json = json.loads(json_)
            tweet_json = {tweet_json['message_id']: {"text": tweet_json['text'], "node_id": tweet_json['node_id']}}
            terms_data_list = termsData.split("\n")
            try:
                terms_data_list.remove('')
            except:
                ""

            matched_phrase_in_tweet = self.matchingFunctions.checkPhraseInTweet(terms_data_list, [tweet_json])
            if len(matched_phrase_in_tweet.keys()) > 0:
                yield matched_phrase_in_tweet

    def findPhraseInTweet(self):

        """
        This method combines the previous two methods since the returning object for terms is a generator; it has to
        be iterated to retrieve data; hence the purpose of this method. Iterating through the terms data, we run
        the method to match the tweet.

        :return: Generator containing all matched terms in the tweets data.
        """
        f = open('%s.txt' % self.termFileName)
        for idx, chunk in enumerate(self.readFileInChunk(f)):
            print("----", idx)
            yield self.readTweets(chunk)

    def matchTweetWithNode(self, matchedTweet):
        """

        This method takes the matched tweets and cross checks whether this appears in nodes data.

        :param matchedTweet: Dictionary containing terms with the corresponding message/mode id.
        :return: Generator with tweets that have matched node_id
        """
        f = open('%s.txt' % self.nodeFile)
        for idx, chunk in enumerate(self.readFileInChunk(f)):
            breakouts = chunk.split("\n")
            try:
                breakouts.remove('')
            except:
                ""
            yield self.matchingFunctions.matchingNodeIdFromTweet(matchedTweet, breakouts)

    def findTweetNodeMatch(self):
        """
        This method combines the previous two methods as they both yield generators and have to be iterated
        to retrieve data.
        :return: matched terms with node_id data that was passed.
        """
        for phraseTweet in (self.findPhraseInTweet()):
            for phrase_ in phraseTweet:
                yield self.matchTweetWithNode(phrase_)

    def dumpData(self):
        """
        This method dumps the data into a local file following the format term, message_id per line.
        :return: None
        """
        f = open("%s.txt" % self.fileToSave, "w")
        matched_term_message = self.findTweetNodeMatch()
        for list_of_terms_nest in matched_term_message:
            for list_of_terms in list_of_terms_nest:
                for term_message in list_of_terms:
                    f.write("%s,%s \n" % (term_message[0][0], term_message[0][1]))
        f.close()
