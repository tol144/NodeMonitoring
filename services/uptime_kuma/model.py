from pydantic import BaseModel


class NodeModel(BaseModel):
    name: str
    ip: str


class AlertDataModel(BaseModel):
    message: str
    ip: str


class AlertData:
    ok = 'ok'
    fail = 'fail'
