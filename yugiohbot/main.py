import os

from page import Page


def function(event, context):
    access_token = os.getenv('ACCESS_TOKEN')
    page_id = os.getenv('PAGE_ID')
    reaction_threshold = int(os.getenv('REACTION_THRESHOLD', 10))
    album_id = os.getenv('ALBUM_ID')

    page = Page(access_token=access_token, id=page_id)

    posts = page.get_posts()  # Get posts from the last week (default)
    print('Got the following posts: ', end=" ")
    print(posts)

    reactions = page.post_reactions(posts)  # Tally up the reactions
    print('Got the following reactions: ', end=" ")
    print(reactions)

    reactions = get_top_reactions(reactions, reaction_threshold)

    booster_pack = create_booster_pack(reactions)

    if len(booster_pack) == 0:
        print('No images in booster pack. All done here!')
        return None

    images = []
    for i, id in enumerate(booster_pack):
        try:
            title = page.own_comments(id)[0].splitlines()[0].split(':')[1].strip()
        except IndexError:
            title = 'Oops, bot broke - Error in post comment, maybe a botmin should check it out?'
        images.append({'url': page.get_post_image(id), 'permalink': page.get_post_permalink(id), 'title': title,
                       'total': reactions[i]['total']})

    print('Image URLS with their titles and totals', end=" ")
    print(images)

    page.post_album(images, album_id)


def get_top_reactions(reactions, threshold):
    """
    We get all the posts with reactions above a threshold.
    If there are > 5 posts, we take those 5.
    Any more than 9 posts, we take the top 9.
    :param reactions: List of reactions for each post.
    :param threshold: The minimum number of reactions for the post to be considered for the booster pack.
    :return: The sorted and filtered list of reactions above the threshold.
    """
    reactions.sort(key=lambda x: x['total'], reverse=True)
    print('Sorted total high to low: ', end=" ")
    print(reactions)

    reactions = list(filter(lambda item: item['total'] >= threshold, reactions))
    print(f'Posts above threshold of {threshold}:', end=" ")
    print(reactions)

    return reactions


def create_booster_pack(reactions):
    """
    Creates the list of post IDs for the booster pack.
    :param reactions: List of sorted reactions.
    :return: The list of post IDs.
    """
    booster_pack = []
    if len(reactions) >= 9:
        booster_pack = reactions[:9]
    elif 5 <= len(reactions) < 9:
        booster_pack = reactions[:5]

    for i, post in enumerate(booster_pack):
        booster_pack[i] = post['id']

    print(f'Post IDs above threshold:', end=" ")
    print(booster_pack)

    return booster_pack
