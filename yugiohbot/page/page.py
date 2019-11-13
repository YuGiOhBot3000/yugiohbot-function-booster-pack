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

    def post_reactions(self, posts):
        reactions_per_post = []
        for post in posts:
            id = post['id']
            r = {'LIKE': 0, 'LOVE': 0, 'HAHA': 0, 'WOW': 0, 'SAD': 0, 'ANGRY': 0}
            reactions = self.graph.get_connections(id=id, connection_name='reactions')

            for reaction in reactions['data']:
                r_type = reaction['type']
                r[r_type] = r.get(r_type) + 1

            while 'paging' in reactions and 'next' in reactions['paging']:
                try:
                    for reaction in reactions['data']:
                        r_type = reaction['type']
                        r[r_type] = r.get(r_type) + 1

                    reactions = requests.get(reactions['paging']['next']).json()
                except KeyError:
                    print(f'Reached end of reactions list.')
                    break

            total = 0
            for r_type in r:
                total += r[r_type]

            reactions_per_post.append({'id': id, 'reactions': r, 'total': total})

        return reactions_per_post

    def post_image(self, post_id):
        image = self.graph.get_connections(id=post_id, connection_name='attachments')
        return image['data'][0]['media']['image']['src']

    def own_comments(self, post_id):
        post = self.graph.get_connections(id=post_id, connection_name='comments')
        comments = []
        for comment in post['data']:
            if comment['from']['id'] == self.id:
                comments.append(comment['message'])

        return comments
