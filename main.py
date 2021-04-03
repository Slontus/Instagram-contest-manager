from instabot import Bot
import re
import os
from dotenv import load_dotenv
import pprint
import argparse


def get_user_names(comment_text):
    """
    The following regular expression pattern for extracting instagram usernames was taken from:
    https://blog.jstassen.com/2016/03/code-regex-for-instagram-username-and-hashtags/
    """
    pattern = re.compile(
        r"""
            (?:@)                                 #matches initial @
            ([a-z\d_]                             #first symbol after @ should be letter, digit or _
            (?:(?:[a-z\d_]|(?:\.(?!\.))?){0,28}   #0 to 28 symbols, no trailing dots allowed
            (?:[a-z\d_]))?)                       #0 or 1 final sybol, not a dot
            """, re.VERBOSE | re.IGNORECASE)

    result = pattern.findall(comment_text)
    return result


def is_user_exist(bot, user):
    user_id = bot.get_user_id_from_username(user)
    return bool(user_id)


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('link', help='Link to Instagram post')
    parser.add_argument('name', help='Instagram link owner name')
    return parser


def get_unique_users(instagram_users):
    return set(map(int, instagram_users))


if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()
    load_dotenv()
    bot = Bot()
    bot.login(username=os.getenv("INSTAGRAM_USER"), password=os.getenv("INSTAGRAM_PASSWORD"))

    user_id = bot.get_user_id_from_username(args.name)
    followers = get_unique_users(bot.get_user_followers(user_id))
    media_id = bot.get_media_id_from_link(args.link)
    all_comments = bot.get_media_comments_all(media_id)

    candidates = {}
    for comment in all_comments:
        users = get_user_names(comment['text'])
        if any((is_user_exist(bot, user) for user in users)):
            candidate_id = comment['user_id']
            candidate_name = bot.get_username_from_user_id(candidate_id)
            candidates[int(candidate_id)] = candidate_name

    media_likers = get_unique_users(bot.get_media_likers(media_id))
    winners = {candidate for candidate_id, candidate in candidates.items() if candidate_id in (media_likers & followers)}
    pprint.pprint(winners)
