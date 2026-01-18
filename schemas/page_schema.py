from pydantic import BaseModel

class PageBase(BaseModel):
    title: str

    class Config:
        anystr_strip_whitespace = True # strip whitespace from all str fields

class PageCreate(PageBase):
    pass

class PageUpdate(PageBase):
    pass
