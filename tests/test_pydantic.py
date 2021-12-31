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
    snake_name: str = Field(alias="matthewPower", tags=["power_comeon"])
    _private: str = ""

    class Config:
        allow_population_by_field_name = True
        allow_mutation = True
        # We use the Python attribute 'bank_account',
        # but read/write the JSON 'bankAccount'
        fields = {"bank_account": "bankAccount"}


def test_private_fields_should_return_none():
    person = Person(name="kk", snake_name="kkk")
    kk = person.dict()

    assert not hasattr(kk, "_private")


def test_valid_field_should_return():
    person = Person(name="kk", snake_name="kkk")
    kk = person.dict(exclude_unset=True)
    assert not kk.get("bank_account")


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
