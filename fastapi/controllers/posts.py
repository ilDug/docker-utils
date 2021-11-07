from typing import List
from models.blog import PostModel
import pymongo
from fastapi import HTTPException
from config.conf import MONGO_BLOG
from pymongo import MongoClient
from models.blog import PostModel



class Posts():

    @classmethod
    def items(cls, limit: int = 10, page: int = 1, hidden: bool = False) -> List[PostModel]:
        hidden = {"hidden": False} if not hidden else None
        with MongoClient(MONGO_BLOG) as c:
            post_num = limit  # numero di post da caricare
            start_from = (page - 1) * limit  # base 0 == OFFSET
            res = c.blog.posts.find(hidden).sort(
                'postid', pymongo.DESCENDING).limit(post_num).skip(start_from)
            posts = [PostModel(**p) for p in res]
            return posts

    @classmethod
    def count(cls, hidden: bool = False) -> int:
        hidden = {"hidden": False} if not hidden else None
        with MongoClient(MONGO_BLOG) as c:
            num = c.blog.posts.count(hidden)
            return num

    @classmethod
    def load(cls,  postid: int, hidden: bool = False) -> PostModel:
        filter = {'postid': postid}
        if not hidden:
            filter['hidden'] = False

        with MongoClient(MONGO_BLOG) as c:
            p = c.blog.posts.find_one(filter)
            if p is None:
                raise HTTPException(404, "Post non trovato")
            post = PostModel(**p)
            return post

    @classmethod
    def add(cls, post: PostModel) -> PostModel:
        with MongoClient(MONGO_BLOG) as c:
            postid = cls.next_postid()
            post.postid = postid
            id = c.blog.posts.insert_one(post.dict()).inserted_id
            return cls.load(postid, True)

    @classmethod
    def edit(cls, post: PostModel, postid: int) -> PostModel:
        with MongoClient(MONGO_BLOG) as c:
            res = c.blog.posts.replace_one(
                {'postid': postid}, post.dict(exclude={'_id'}))
            if res.matched_count <= 0:
                raise HTTPException(400, "l'id non corrisponde a nessun post")
            if res.modified_count <= 0:
                raise HTTPException(500, "errori di modifica del post")
            return cls.load(postid, True)

    @classmethod
    def remove(cls, postid: int) -> bool:
        with MongoClient(MONGO_BLOG) as c:
            res = c.blog.posts.delete_one({'postid': postid})
            return res.deleted_count > 0

    # trova il valore più alto dei postid e ritorna l'intero successivo
    @classmethod
    def next_postid(cls):
        with MongoClient(MONGO_BLOG) as c:
            cursor = c.blog.posts.aggregate([{
                '$group': {
                    '_id': None,
                    'max': {'$max': '$postid'}
                }
            }])
            results = [res['max'] for res in cursor]
            next = int(results.pop(0)) + 1
            return next
