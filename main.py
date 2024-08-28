from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session

# 데이터베이스 URL 설정
DATABASE_URL = "postgresql://user:mysecretpassword@localhost:5432/postgres"

# SQLAlchemy 설정
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# SQLAlchemy 데이터베이스 모델 정의
class PostDB(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    views = Column(Integer, default=0)  # views 필드 추가
    comments = relationship("CommentDB", back_populates="post", cascade="all, delete-orphan")

class CommentDB(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    content = Column(Text, nullable=False)
    post = relationship("PostDB", back_populates="comments")

# Pydantic 모델 정의
class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    pass

class Comment(CommentBase):
    id: int
    post_id: int

    class Config:
        orm_mode = True

class PostBase(BaseModel):
    title: str
    content: str

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    views: int  # views 필드 추가
    comments: List[Comment] = []

    class Config:
        orm_mode = True

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

# FastAPI 애플리케이션 인스턴스 생성
app = FastAPI()

# CORS 설정 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React 앱의 주소를 허용
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용 (GET, POST, PUT, DELETE 등)
    allow_headers=["*"],  # 모든 헤더 허용
)

# 데이터베이스 세션을 가져오는 의존성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 게시물 목록 조회 (GET /posts)
@app.get("/posts", response_model=List[Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(PostDB).order_by(PostDB.id.desc()).all()  # id를 기준으로 내림차순 정렬
    return posts

# 게시물 상세 조회 (GET /posts/{id})
@app.get("/posts/{id}", response_model=Post)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(PostDB).filter(PostDB.id == id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

# 게시물 추가 (POST /posts)
@app.post("/posts", response_model=Post)
def add_post(post: PostCreate, db: Session = Depends(get_db)):
    try:
        new_post = PostDB(title=post.title, content=post.content)
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return new_post
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 게시물 수정 (PUT /posts/{id})
@app.put("/posts/{id}", response_model=Post)
def edit_post(id: int, updated_post: PostCreate, db: Session = Depends(get_db)):
    try:
        post = db.query(PostDB).filter(PostDB.id == id).first()
        if post is None:
            raise HTTPException(status_code=404, detail="Post not found")
        post.title = updated_post.title
        post.content = updated_post.content
        db.commit()
        db.refresh(post)
        return post
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 게시물 삭제 (DELETE /posts/{id})
@app.delete("/posts/{id}", response_model=dict)
def delete_post(id: int, db: Session = Depends(get_db)):
    try:
        post = db.query(PostDB).filter(PostDB.id == id).first()
        if post is None:
            raise HTTPException(status_code=404, detail="Post not found")
        db.delete(post)
        db.commit()
        return {"message": "Post deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 조회수 증가 (PATCH /posts/{id}/views)
@app.patch("/posts/{id}/views", response_model=Post)
def increase_views(id: int, db: Session = Depends(get_db)):
    try:
        post = db.query(PostDB).filter(PostDB.id == id).first()
        if post is None:
            raise HTTPException(status_code=404, detail="Post not found")
        post.views += 1
        db.commit()
        return post
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 댓글 추가 (POST /posts/{id}/comments)
@app.post("/posts/{id}/comments", response_model=Comment)
def add_comment(id: int, comment_data: CommentCreate, db: Session = Depends(get_db)):
    try:
        post = db.query(PostDB).filter(PostDB.id == id).first()
        if post is None:
            raise HTTPException(status_code=404, detail="Post not found")
        
        new_comment = CommentDB(post_id=id, content=comment_data.content)
        db.add(new_comment)
        db.commit()
        db.refresh(new_comment)
        return new_comment
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 댓글 삭제 (DELETE /posts/{id}/comments/{comment_id})
@app.delete("/posts/{id}/comments/{comment_id}", response_model=dict)
def delete_comment(id: int, comment_id: int, db: Session = Depends(get_db)):
    try:
        comment = db.query(CommentDB).filter(CommentDB.id == comment_id, CommentDB.post_id == id).first()
        if comment is None:
            raise HTTPException(status_code=404, detail="Comment not found")
        db.delete(comment)
        db.commit()
        return {"message": "Comment deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
