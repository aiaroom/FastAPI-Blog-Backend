from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    slug: str
    content_html: str
    category_id: int


class PostCreate(PostBase):
    pass


class PostOut(PostBase):
    id: int
    author_id: int

    class Config:
        from_attributes = True
