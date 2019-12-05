import os
import unittest
from unittest import mock
from datetime import datetime, timedelta
import json

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
        image_url = self.page.get_post_image(id)
        self.assertTrue('https' in image_url)

    def test_post_url(self):
        id = '101675587943804_119079029536793'
        image_url = self.page.get_post_permalink(id)
        self.assertTrue('https' in image_url)

    def test_own_comments(self):
        id = '101675587943804_119079029536793'
        comments = self.page.own_comments(id)
        self.assertTrue(len(comments) > 0)

    @mock.patch('facebook.GraphAPI.put_object')
    def test_create_weekly_album(self, mock_put_object):
        expected = '1234'
        mock_put_object.return_value = {'id': expected}
        result = self.page.create_weekly_album()
        self.assertEqual(result, expected)

    @mock.patch('facebook.GraphAPI.put_photo')
    def test_post_album(self, mock_put_photo):
        mock_put_photo.return_value = {'id': 1}
        url = 'https://images-na.ssl-images-amazon.com/images/I/51up1E83ZlL._SX355_.jpg'
        images = [
            {'url': url, 'title': 'test', 'total': 1, 'permalink': url},
            {'url': url, 'title': 'test', 'total': 2, 'permalink': url}
        ]
        result = self.page.post_album(images, '1234', save_location='image.jpg')
        os.remove('image.jpg')
        self.assertEqual(result, [1, 1])


if __name__ == '__main__':
    unittest.main()
