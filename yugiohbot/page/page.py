from datetime import datetime, timedelta

import facebook
import requests


class Page:

    def __init__(self, access_token, id):
        self.graph = facebook.GraphAPI(access_token=access_token)
        self.id = id

    def get_posts(self, days_ago=7):
        posts = self.graph.get_connections(id=self.id, connection_name='posts')
        all_posts = []

        threshold = (datetime.now() - timedelta(days=days_ago))
        if not threshold.hour % 2 == 0:
            threshold = threshold.replace(hour=threshold.hour - 1)
        threshold = threshold.strftime("%Y-%m-%dT%H")

        while 'next' in posts['paging']:
            try:
                for post in posts['data']:
                    all_posts.append(post)
                    if self.__reached_threshold(post, threshold):
                        return all_posts

                posts = requests.get(posts['paging']['next']).json()
            except KeyError:
                print(f'Reached end of post list, or threshold of {threshold}')
                break

        return all_posts

    @staticmethod
    def __reached_threshold(post, threshold):
        return threshold in post['created_time']
