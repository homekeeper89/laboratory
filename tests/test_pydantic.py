import datetime
from decimal import Decimal
from typing import List, NewType, Optional, Set
import json
from pydantic import BaseModel, Field

PersonId = NewType("PersonId", int)


class Person(BaseModel):
    id: PersonId = None
    name: str = None
    bank_account: Decimal = 10
    birthdate: datetime.date = datetime.datetime.now()
    friends: Optional[List[PersonId]] = None
    snake_name: str = Field(alias="matthewPower")

    class Config:
        allow_population_by_field_name = True
        allow_mutation = True
        # We use the Python attribute 'bank_account',
        # but read/write the JSON 'bankAccount'
        fields = {"bank_account": "bankAccount"}


def test_valid_field_should_return():
    person = Person(name="kk", snake_name="kkk")
    kk = person.dict(exclude_unset=True)
    assert not kk.get("bank_account")


def test_wrong_data_should_match_format(test_client, get_token_headers):
    data = {"wrong": "keyword"}
    res = test_client.post(
        "/api/running/body_model", data=json.dumps(data), headers=get_token_headers(1234)
    )
    assert res.status_code == 400
    assert res.json["error"]


def test_body_model_pandatic_should_work(test_client, get_token_headers):
    data = {"some": "data", "end": "data"}
    res = test_client.post(
        "/api/running/body_model", data=json.dumps(data), headers=get_token_headers(1234)
    )
    assert res.status_code == 200


def test_query_model_pandatic_should_work(test_client):
    res = test_client.get("/api/running/query_model?age=1")
    assert res.status_code == 200


def test_exclude_should_work():
    origin = Person(
        id=1,
        name="hello",
        bank_account=11233,
        birthdate=datetime.datetime.now(),
        friends=[1],
        snake_name="name",
    )
    res = origin.dict(exclude={"bank_account", "snake_name"})
    assert not hasattr(res, "bank_account")


def test_two_differ_fields_work():
    origin = Person(
        id=1,
        name="hello",
        bank_account=11233,
        birthdate=datetime.datetime.now(),
        friends=[1],
        snake_name="name",
    )
    assert origin

    diff = Person(
        id=1,
        name="hello",
        bankAccount=11233,
        birthdate=datetime.datetime.now(),
        friends=[1],
        matthewPower="name",
    )
    assert diff
