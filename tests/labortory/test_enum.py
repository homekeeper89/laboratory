import pytest
from app.core.database.models import User, LabModel
from app.domains.laboratory.enum import BasicEnum, AdvancedStrEnum, Enum


def test_adv_enum_should_same_type_to_str():
    assert BasicEnum.HELLO_WORLD.value == "HELLO_WORLD"
    assert AdvancedStrEnum.HELLO_WORLD == "HELLO_WORLD"
    assert AdvancedStrEnum.HELLO_WORLD == BasicEnum.HELLO_WORLD.value

    assert isinstance(BasicEnum.HELLO_WORLD.value, str)
    assert not isinstance(BasicEnum.HELLO_WORLD.value, Enum)

    assert isinstance(AdvancedStrEnum.HELLO_WORLD, str)
    assert isinstance(AdvancedStrEnum.HELLO_WORLD, Enum)


@pytest.mark.xfail(reason="enum 으로 저장이 되서 fail 남")
def test_enum_should_save_in_db(lab_session):
    lab_model = LabModel(nickname=BasicEnum.HELLO_WORLD.value)
    lab_session.add(lab_model)
    lab_session.commit()

    res = lab_session.query(LabModel).first()
    assert res.nickname == BasicEnum.HELLO_WORLD.value

    # sqlalchemy.exc.ProgrammingError: (mysql.connector.errors.ProgrammingError) Failed processing pyformat-parameters; Python 'advancedstrenum' cannot be converted to a MySQL type
    lab_model = LabModel(nickname=AdvancedStrEnum.HELLO_WORLD)
    lab_session.add(lab_model)
    lab_session.commit()

    res = lab_session.query(User).all()[-1]
    assert res.nickname == AdvancedStrEnum.HELLO_WORLD
