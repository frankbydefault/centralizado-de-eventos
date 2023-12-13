import instaloader
import datetime
from dotenv import load_dotenv
import os

load_dotenv()
L = instaloader.Instaloader()

USER = os.getenv('INSTAGRAM_USER')
L.load_session_from_file(USER)

accounts = ["hubprovidencia","munilascondes","vitacura_","munistgo"]
results = []

# Devuelve una lista con cada post y su cuenta de procedencia
def fetch_posts():
    today = datetime.date.today()

    for account in accounts:
        profile = instaloader.Profile.from_username(L.context, account)

        for post in profile.get_posts():
            post_date = post.date.date()

            if post_date == today:
                description = post.caption
                obj = {
                    "account": account,
                    "post": description,
                }
                results.append(obj)
            else: 
                break

    return results

