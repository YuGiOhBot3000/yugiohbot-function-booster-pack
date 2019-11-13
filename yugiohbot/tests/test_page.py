import os
import unittest
from datetime import datetime, timedelta

from page import Page


class TestPage(unittest.TestCase):
    def setUp(self):
        access_token = os.getenv('ACCESS_TOKEN')
        page_id = os.getenv('PAGE_ID')
        self.page = Page(access_token=access_token, id=page_id)

    def test_get_posts(self):
        days_ago = 7
        expected_final_date = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")
        posts = self.page.get_posts(days_ago=days_ago)
        self.assertTrue(expected_final_date in posts[len(posts) - 1]['created_time'])

    def test_post_reactions(self):
        posts = self.page.get_posts(days_ago=1)
        reactions = self.page.post_reactions(posts)
        self.assertTrue(len(reactions) > 0)

    def test_post_image(self):
        id = '101675587943804_119079029536793'
        image_url = self.page.post_image(id)
        self.assertTrue('https' in image_url)

    def test_own_comments(self):
        id = '101675587943804_119079029536793'
        comments = self.page.own_comments(id)
        self.assertTrue(len(comments) > 0)


if __name__ == '__main__':
    unittest.main()
