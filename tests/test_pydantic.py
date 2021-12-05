import datetime
from decimal import Decimal
from typing import List, NewType, Optional, Set

from pydantic import BaseModel, Field

PersonId = NewType("PersonId", int)


class Person(BaseModel):
    id: PersonId
    name: str
    bank_account: Decimal
    birthdate: datetime.date
    friends: Optional[List[PersonId]] = None
    snake_name: str = Field(alias="matthewPower")

    class Config:
        allow_population_by_field_name = True
        allow_mutation = True
        # We use the Python attribute 'bank_account',
        # but read/write the JSON 'bankAccount'
        fields = {"bank_account": "bankAccount"}


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

