import os
import random
import string
from sqlalchemy.orm import sessionmaker
import requests
from bs4 import BeautifulSoup
from image import create_image_using_comments

## HackerNews APIs
BEST_STORIES_URI = "https://hacker-news.firebaseio.com/v0/beststories.json"
STORY_RESOURCE_URI = "https://hacker-news.firebaseio.com/v0/item/"
HACKERNEWS_URL_1PG = "https://news.ycombinator.com"
HACKERNEWS_URL_2PG = "https://news.ycombinator.com/news?p=2"

BASE_DIR = os.getcwd()


def get_hackernews_data():

    # Get hackernews 2 pages html

    hn_response1 = requests.get(HACKERNEWS_URL_1PG)
    hn_response2 = requests.get(HACKERNEWS_URL_2PG)

    if hn_response1.status_code == 200:
        hn1_soup = BeautifulSoup(hn_response1.text, 'html.parser')

    if hn_response2.status_code == 200:
        hn2_soup = BeautifulSoup(hn_response2.text, 'html.parser')
    
    all_scores_text = hn1_soup.find_all('span', 'score') + hn2_soup.find_all('span', 'score')


    # fetch ids where score >= 200

    latest_hn_top_ids = []
    new_post_id_list = []

    for score_text in all_scores_text:
        if " points" in score_text.text:
            score = int(score_text.text.replace(" points", ""))

            if score >= 200:

                if "score_" in score_text["id"]:

                    hn_news_id = score_text["id"].replace("score_", "")

                    latest_hn_top_ids.append(str(int(hn_news_id)))

    if latest_hn_top_ids:

        latest_hn_top_ids = list(set(latest_hn_top_ids))

        # save story IDs in a sqlite database
        Session = sessionmaker(bind=db_engine)
        db_session = Session()

        for hn_news_id in latest_hn_top_ids:
            post_exists = db_session.query(HackernewsBest).filter(HackernewsBest.news_id==hn_news_id).first()

            if not post_exists:
                new_post = HackernewsBest(news_id=hn_news_id)
                db_session.add(new_post)
                new_post_id_list.append(hn_news_id)

        db_session.commit()

    return new_post_id_list


def get_top_comment_data(comments_ids):

    comments_text = []
    for ids in comments_ids:

        comment_res = requests.get(STORY_RESOURCE_URI + str(ids) + '.json')

        if comment_res.status_code == 200:
            if comment_res.json()['type'] == 'comment':
                plain_text = BeautifulSoup(comment_res.json()['text'].replace("\n", "").replace("<p>", "\n"), "html.parser").get_text()
                comments_text.append(plain_text)

    return comments_text


def get_summary_new_posts(new_post_ids):

    for post_id in new_post_ids:

        ## Download data and create image

        FOLDER_PATH =  os.path.join(BASE_DIR, 'hn-summary')
        temp_filename = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(32)) + ".png"
        temp_filename = os.path.join(FOLDER_PATH, temp_filename)

        try:

            story_res = requests.get(STORY_RESOURCE_URI + str(news_id) + '.json')

            if story_res.status_code == 200:
                if story_res.json()['type'] == 'story':

                    # check if time passed is > 24 hours
                    days = (datetime.now() - datetime.fromtimestamp(int(story_res.json()['time']))).days

                    if not days == 0:  # TODO: need to fix
                        return False

                    if int(story_res.json()['score']) >= 200:

                        # collect 2 kids data to get top 2 comments
                        if 'kids' in story_res.json():
                            if len(story_res.json()['kids']) > 2:
                                # prepare comments and create image
                                story_title = story_res.json()['title']
                                comments_text = get_top_comment_data(story_res.json()['kids'][:2])

                                create_image_using_comments(temp_filename, story_title, comments_text)

                            else:
                                return False
                        else:
                            return False
                    else:
                        return False
                else:
                    return False
            else:
                return False

        except:
            return False

    return True