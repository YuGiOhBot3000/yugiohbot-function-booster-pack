from datetime import datetime, timedelta

import facebook
import requests


class Page:

    def __init__(self, access_token, id):
        self.graph = facebook.GraphAPI(access_token=access_token, version='8.0')
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
            r = {'like': 0, 'love': 0, 'haha': 0, 'wow': 0, 'sorry': 0, 'anger': 0}
            reactions = self.graph.get_connections(id=id, connection_name='insights/post_reactions_by_type_total')

            if 'data' in reactions and len(reactions['data']) > 0:
                data = reactions['data'][0]
                values = data['values']

                if len(values) > 0:
                    value = values[0]['value']

                    for type, count in value.items():
                        r[type] = r.get(type) + count

                    while 'paging' in reactions and 'next' in reactions['paging']:
                        try:
                            reactions = requests.get(reactions['paging']['next']).json()

                            if 'data' in reactions and len(reactions['data']) > 0:
                                data = reactions['data'][0]
                                values = data['values']

                                if len(values) > 0:
                                    value = values[0]['value']

                                    for type, count in value.items():
                                        r[type] = r.get(type) + count

                        except KeyError:
                            print(f'Reached end of reactions list.')
                            break

                    total = 0
                    for r_type in r:
                        total += r[r_type]

                    reactions_per_post.append({'id': id, 'reactions': r, 'total': total})

        return reactions_per_post

    def get_post_image(self, post_id):
        image = self.graph.get_connections(id=post_id, connection_name='attachments')
        return image['data'][0]['media']['image']['src']

    def get_post_permalink(self, post_id):
        image = self.graph.get_object(id=post_id, fields='permalink_url')
        return image['permalink_url'].split('?substory_index')[0]

    def own_comments(self, post_id):
        post = self.graph.get_connections(id=post_id, connection_name='comments')
        comments = []
        for comment in post['data']:
            if 'from' in comment:
                if comment['from']['id'] == self.id:
                    comments.append(comment['message'])

        return comments

    def post_album(self, images, album_id, save_location='/tmp/image.jpg'):
        post_ids = []

        for image in images:
            message = f'Card Name: {image["title"]}\nTotal Reactions: {image["total"]}\nOriginal Post: {image["permalink"]}'
            print(message)
            r = requests.get(image['url'])

            f = open(save_location, 'wb')
            f.write(r.content)
            f.close()

            f = open(save_location, 'rb')
            post = self.graph.put_photo(image=f, message=message, album_path=album_id + "/photos")
            f.close()

            post_ids.append(post['id'])

        return post_ids
