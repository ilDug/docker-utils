from controllers.posts import Posts
from pymongo import MongoClient, cursor
from models.blog import PostViewModel,  PostModel
from datetime import datetime
from config.conf import MONGO_BLOG
from pydantic import IPvAnyAddress


class Views(Posts):

    @classmethod
    def add_views(cls,  postid: int, ip: IPvAnyAddress = None):
        view = PostViewModel(postid=postid, ip=ip, date=datetime.utcnow())
        with MongoClient(MONGO_BLOG) as c:
            id = c.blog.views.insert_one(view.dict()).inserted_id
        return str(id)

    @classmethod
    def views(cls,  postid: int):
        with MongoClient(MONGO_BLOG) as c:
            res = c.blog.views.aggregate([
                {"$match": {"postid": postid}},
                {"$group": {"_id": "postid", "views": {"$sum": 1}}},
            ])
            views = [v['views'] for v in res]

        return views.pop()

    @classmethod
    def populars(cls, limit: int = 4):
        with MongoClient(MONGO_BLOG) as c:
            # cerca i primi postid in base alle visualizzazione
            cursor = c.blog.views.aggregate([
                {"$group": {"_id": "$postid", "views": {"$sum": 1}}},
                {"$sort": {"views": -1}},
                {"$limit": 4},
                {"$lookup": {
                    "from": "posts",
                    "localField": "_id",
                    "foreignField": "postid",
                    "as": "posts"
                }},
                {"$replaceRoot": {"newRoot": {"$mergeObjects": [
                    "$$ROOT",
                    {"$arrayElemAt": ["$posts", 0]},
                ]}}},
                {"$project": {"posts": 0}},
            ])

            results = [PostModel(**p) for p in cursor]
            return results

            # # estrae la list degli id dei post
            # popular_ids = [p["_id"] for p in results]

            # # cerca i post in base ai postid
            # posts = c.blog.posts.find({"postid": {"$in": popular_ids}})

            # # unisce i post alle visualizzazioni
            # populars = [
            #     PostModel(**pop,
            #               views=next(x['views'] for x in results if x['_id'] == pop['postid']))
            #     for pop in posts]

            # # ordina in base alle visualizzazioni
            # populars.sort(reverse=True, key=lambda x: x.views)
            # return populars
