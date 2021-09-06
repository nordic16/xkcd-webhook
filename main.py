if __name__ == '__main__':
    from discord_webhook import DiscordWebhook, DiscordEmbed
    from datetime import datetime, timedelta
    import requests, time, random
    import config


    def get_latest_comic_num() -> int:
        json = requests.get('https://xkcd.com/info.0.json').json()

        return int(json['num'])


    """
    This works by first retrieving the latest comic
    with the intent of getting the number of existent comics (x).

    After doing that, use that number to generate a random number (let's call it y)
    between 1 and x. Then retrieve the comic whose id is y.
    """
    def send_random_comic():
        webhook = DiscordWebhook(url=config.URL)
        webhook.avatar_url = "https://pbs.twimg.com/profile_images/1364920241265012743/Y__158zv.png"

        max = get_latest_comic_num()
        rand = random.randrange(1, max + 1)

        comic = requests.get(f'https://xkcd.com/{rand}/info.0.json').json()
        embed = create_embed(comic)

        webhook.add_embed(embed)
        webhook.execute()


    """
    Returns an embed according to comic
    """
    def create_embed(comic) -> DiscordEmbed:
        embed = DiscordEmbed(title=comic['title'], description=comic['alt'], color=242424)
        embed.set_image(url=comic['img'])

        return embed


    while True:
        send_random_comic()

        waitTime = datetime.now()  + timedelta(hours=5)

        while datetime.now() < waitTime:
            time.sleep(1)
