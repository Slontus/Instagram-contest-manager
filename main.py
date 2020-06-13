from instabot import Bot
import re
import os
from dotenv import load_dotenv
import pprint
import argparse


def get_user_names(comment_text):
    pattern = re.compile(r"(?:@)([a-z\d_](?:(?:[a-z\d_]*|(?:\.(?!\.)){0,1}){0,28}(?:[a-z\d_]))?)", flags=re.I)
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


def get_unique_results(bot_method, source):
    results = bot_method(source)
    return set(map(int, results))


if __name__ == "__main__":
    parser = create_parser()
    link = (args := parser.parse_args()).link
    user_name = args.name
    load_dotenv()
    bot = Bot()
    bot.login(username=os.getenv("USER"), password=os.getenv("PASSWORD"))

    user_id = bot.get_user_id_from_username(user_name)
    followers = get_unique_results(bot.get_user_followers, user_id)
    media_id = bot.get_media_id_from_link(link)
    all_comments = bot.get_media_comments_all(media_id)

    candidates = []
    for comment in all_comments:
        users = get_user_names(comment['text'])
        if any([is_user_exist(bot, user) for user in users]):
            candidate_name = bot.get_username_from_user_id(candidate_id := comment['user_id'])
            candidates.append((int(candidate_id), candidate_name))

    media_likers = get_unique_results(bot.get_media_likers, media_id)
    winners = [candidate[1] for candidate in candidates if candidate[0] in (media_likers & followers)]
    winners = set(winners)
    pprint.pprint(winners)
