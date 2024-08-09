from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# 데이터 모델
class Post(BaseModel):
    id: int
    title: str
    content: str

class Comment(BaseModel):
    id: int
    post_id: int
    content: str

# 임시 데이터베이스 (메모리 내 데이터베이스)
posts = []
comments = []

# 게시물 목록 조회 (GET /posts)
@app.get("/posts", response_model=List[Post])
def get_posts():
    return posts

# 게시물 상세 조회 (GET /posts/{id})
@app.get("/posts/{id}", response_model=Post)
def get_post(id: int):
    post = next((post for post in posts if post.id == id), None)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

# 게시물 추가 (POST /posts)
@app.post("/posts", response_model=Post)
def add_post(post: Post):
    posts.append(post)
    return post

# 게시물 수정 (PUT /posts/{id})
@app.put("/posts/{id}", response_model=Post)
def edit_post(id: int, updated_post: Post):
    for index, post in enumerate(posts):
        if post.id == id:
            posts[index] = updated_post
            return updated_post
    raise HTTPException(status_code=404, detail="Post not found")

# 게시물 삭제 (DELETE /posts/{id})
@app.delete("/posts/{id}", response_model=dict)
def delete_post(id: int):
    global posts
    posts = [post for post in posts if post.id != id]
    return {"message": "Post deleted successfully"}

# 댓글 추가 (POST /posts/{id}/comments)
@app.post("/posts/{id}/comments", response_model=Comment)
def add_comment(id: int, comment: Comment):
    if not any(post.id == id for post in posts):
        raise HTTPException(status_code=404, detail="Post not found")
    comments.append(comment)
    return comment

# 댓글 삭제 (DELETE /posts/{id}/comments/{comment_id})
@app.delete("/posts/{id}/comments/{comment_id}", response_model=dict)
def delete_comment(id: int, comment_id: int):
    global comments
    comments = [comment for comment in comments if not (comment.post_id == id and comment.id == comment_id)]
    return {"message": "Comment deleted successfully"}
