from collections import defaultdict
import itertools
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class MatchingPhrase:
    message_id: str
    node_id: str


class MatchingFunctions():
    """

    Functions used to match term -> tweet -> node

    """

    def isConsecutive(self, indexList) -> bool:
        """
        Method returning whether a list of numbers are consecutive
        :param indexList: list of numbers
        :return: True/False
        """
        indexList = list(indexList)
        return indexList == list(range(min(indexList), max(indexList) + 1))

    def phraseInSentence(self, sentence, phrase) -> bool:
        """
        Method that returns whether a phrase appears in a sentence order matters.
        :param sentence: Sentence Dict that contains index
        :param phrase: Phrases to check
        :return: True/False
        """
        word_in_setence_list = []
        for word in phrase:
            try:
                # HERE WE MAKE THE PHRASE WORD LOWER.
                word_in_setence_list.append(sentence[word.lower()])
            except:
                break
        all_combination = list(itertools.product(*word_in_setence_list))
        # word in phrase can appear multiple times in the tweet; here we are only considered whether they appear consecutively.
        is_combo = [self.isConsecutive(combo) for combo in all_combination]

        return True in is_combo

    def checkPhraseInTweet(self, phrase_list, tweet_dic_list) -> Dict[str, List[MatchingPhrase]]:
        """
        This method is the heart of the analysis.
        The premise is to find the cross match of a list of phrases with a list of dictionary of tweets; returning a
        list of Data Class with the message_id and node_id from the tweet that matches.

        :param phrase_list: A list of terms
        :param tweet_dic_list: A Dictionary containing the message_id, text and node_id.
        :return: List of Data Class of the tweet and its message_id and node_id.
        """
        matched_dic = defaultdict(list)
        index_of_word_in_sentence_list = []
        all_index_in_sentence = defaultdict(list)

        phrase_dict_list = [{k: v for v, k in enumerate(sentence.split())} for sentence in phrase_list]

        # The iteration below is to capture the index of word in the each tweet. This dictionary is appended to a list.
        # The list and dictionary is used to find whether the phrase appears in the tweet.
        for sentence in tweet_dic_list:
            word_in_sentence_dic = defaultdict(list)
            first_key_dic = next(iter(sentence.values()))
            first_key_text_list = first_key_dic['text'].split()

            for idx, word in enumerate(first_key_text_list):
                # HERE WE MAKE THE WORD LOWER IN TEXT
                word_in_sentence_dic[word.lower()].append(idx)
            index_of_word_in_sentence_list.append(word_in_sentence_dic)

        # The dictionary below is used to check whether a word appears in the sentence. The premise of this dictionary
        # is that we do not want to run the function to check the phrase is the same in the sentence if the word in the
        # phrase does not appear in the sentence.
        for index, word_dic in enumerate(index_of_word_in_sentence_list):
            for idx, word in enumerate(word_dic.keys()):
                all_index_in_sentence[word].append(index + 1)

        for idx, phrase in enumerate(phrase_dict_list):

            indexOfWordAppearance = None
            lenOfTweetSentence = len(index_of_word_in_sentence_list) + 1

            for word in phrase.keys():
                word = word.lower()
                if lenOfTweetSentence > len(all_index_in_sentence[word]):
                    lenOfTweetSentence = len(all_index_in_sentence[word])
                    indexOfWordAppearance = all_index_in_sentence[word]

            for index in indexOfWordAppearance:
                matched = self.phraseInSentence(index_of_word_in_sentence_list[index - 1], phrase)

                if matched:
                    message_id_json = tweet_dic_list[index - 1]
                    first_key = next(iter(message_id_json.keys()))
                    message_tuple = MatchingPhrase(first_key, message_id_json[first_key]['node_id'])
                    matched_dic[phrase_list[idx]].append(message_tuple)
        return dict(matched_dic)

    def filterValueBasedOnTuple(self, keyword, matchingPhraseDc, list_of_criteria_to_map):
        """
        In this method, we look at whether the node_id appears in the MatchingPhrase Data Class; returning the
        term and the message_id

        :param keyword: term
        :param matchingPhraseDc:  dataclass of MatchingPhrase.
        :param list_of_criteria_to_map: list of node_id
        :return: generator with term, message_id
        """
        for value in list_of_criteria_to_map:
            for phrase in matchingPhraseDc:
                if phrase.node_id == value:
                    yield keyword, phrase.message_id

    def matchingNodeIdFromTweet(self, matched_text_message_node_id: Dict[str, List[MatchingPhrase]],
                                node_id_to_match_list):
        """
        This method first checks if the node_id appears in the list of node_id and then runs the function to find
        the corresponding term,message_id.

        :param matched_text_message_node_id: Dictionary with dataclass of MatchingPhrase
        :param node_id_to_match_list:
        :return: generator that contains the matched term,message_id
        """
        for key in matched_text_message_node_id.keys():
            list_of_node_id_matched = []
            for tuple_ in matched_text_message_node_id[key]:
                list_of_node_id_matched.append(tuple_.node_id)
            intersecting_node_id_list = (set(list_of_node_id_matched) & set(node_id_to_match_list))
            if len(intersecting_node_id_list) > 0:
                yield list(
                    self.filterValueBasedOnTuple(key, matched_text_message_node_id[key], intersecting_node_id_list))
