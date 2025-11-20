
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from datetime import date

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Post(BaseModel):
    id: int = Field(title="The ID of the post", ge=1)
    name: str = Field(title="The name of the post", min_length=1)
    description: str = Field(title="The description of the post", min_length=1)
    created_at: date = Field(title="The date the post was created")

class PostRequest(BaseModel):
    name: str
    description: str

class PostResponse(BaseModel):
    id: int
    name: str
    description: str
    created_at: date

posts = [
    {"id": 1, "name": "Post 1", "description": "This is the first post", "created_at": date(2024, 7, 1)},
    {"id": 2, "name": "Post 2", "description": "This is the second post", "created_at": date(2024, 7, 2)},
]

@app.get("/health")
async def health():
    return {"status": "Healthy"}

@app.post("/posts")
async def create_post(post: PostRequest):
    new_post = {"id": len(posts) + 1, "name": post.name, "description": post.description, "created_at": date.today()}
    posts.append(new_post)
    return new_post

@app.get("/posts")
async def read_posts():
    return posts

@app.put("/posts/{post_id}")
async def update_post(post_id: int, post: PostRequest):
    post_to_update = None
    for p in posts:
        if p['id'] == post_id:
            post_to_update = p
            break
    if post_to_update:
        post_to_update['name'] = post.name
        post_to_update['description'] = post.description
        return post_to_update
    return {"error": f"Post with id {post_id} not found"}

@app.delete("/posts/{post_id}")
async def delete_post(post_id: int):
    global posts
    posts = [p for p in posts if p['id'] != post_id]
    return {"message": f"Post with id {post_id} deleted"}
