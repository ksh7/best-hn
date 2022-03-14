from huey import SqliteHuey, crontab

from hackernews import get_hackernews_data, get_summary_new_posts
from twitter import random_post_to_tweet

huey = SqliteHuey(filename='huey_tasks.db')


@huey.periodic_task(crontab(minute='*/2'))
def fetch_every2_hours():
	"""
		Fetch top posts every 2 hours
	"""

	new_post_ids = get_hackernews_data() # get new stories reaching > 200 score in last 2 hours
	get_summary_new_posts(new_post_ids) # create summary of new posts
