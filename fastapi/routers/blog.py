from typing import List, Optional
from controllers.parser import Parser
from models.blog import PostModel
from controllers.views import Views
from controllers.posts import Posts
from fastapi import APIRouter, Header, Query, Path, Body, Depends
from middlewares.auth import admin_guard, authentication_guard
from middlewares.post_filters import hidden_posts

router = APIRouter(
    tags=['blog'],
    dependencies=[]
)


@router.get("/blog/posts")
async def posts(
    l: int = Query(10, title="limit",
                   description="limite di post da caricare"),
    p: int = Query(1, title="page",
                   description="i post vengono caricati in gruppi,  ogni gruppo contiente un numero di posts uguale a limit"),
    hidden: bool = Depends(hidden_posts)
):
    return Posts().items(l, p, hidden)


@router.get("/blog/posts/populars")
async def posts(l: Optional[int] = Query(4, title="limit", description="limite di populars da caricare")):
    return Views().populars(l)


@router.get("/blog/posts/count")
async def posts(hidden: bool = Depends(hidden_posts)):
    return Posts().count(hidden)


@router.get("/blog/posts/{postid}")
async def get_post(postid: int = Path(None), hidden: bool = Depends(hidden_posts)):
    return Posts().load(postid, hidden)


@router.post("/blog/posts",  dependencies=[Depends(authentication_guard), Depends(admin_guard)])
async def add_post(post: PostModel = Body(...)):
    return Posts().add(post)


@router.put("/blog/posts/{postid}",  dependencies=[Depends(authentication_guard), Depends(admin_guard)])
async def add_post(post: PostModel = Body(...), postid: int = Path(...)):
    return Posts().edit(post, postid)


@router.delete("/blog/posts/{postid}",  dependencies=[Depends(authentication_guard), Depends(admin_guard)])
async def add_post(postid: int = Path(...)):
    return Posts().remove(postid)


# async def parse_post(posts_list: List[PostModel] = Body(...)):
# @router.post("/blog/parse",  dependencies=[Depends(authentication_guard), Depends(admin_guard)])
# async def parse_post():
#     return Parser().parse()


############################################################
# VIEWS
############################################################
@router.get("/blog/posts/{postid}/views")
async def get_post(postid: int = Path(None)):
    return Views().views(postid)


@router.post("/blog/posts/{postid}/views")
async def get_post(postid: int = Path(None), x_real_ip: Optional[str] = Header(None)):
    return Views().add_views(postid, x_real_ip)
