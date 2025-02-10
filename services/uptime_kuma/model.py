from pydantic import BaseModel


class NodeModel(BaseModel):
    name: str
    ip: str


class AlertDataModel(BaseModel):
    message: str
    node_name: str


class AlertData:
    ok = 'ok'
    fail = 'fail'
