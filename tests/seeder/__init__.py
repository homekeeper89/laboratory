from faker import Factory as FakerFactory

import factory
from app.core.database.models import Running, RunningConfig, RunningParticipant, User
from app.domains.running.enum import (
    RunningConfigCategoryEnum,
    RunningStatusEnum,
    RunningModeEnum,
    RunningCategoryEnum,
    RunningParticipantEnum,
)

faker = FakerFactory.create(locale="ko_KR")


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User

    nickname = factory.lazy_attribute(lambda x: faker.name() + "_nick")
    status = "active"


class RunningFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Running

    user_id = factory.lazy_attribute(lambda x: faker.random_int(1, 100000))
    category = factory.lazy_attribute(
        lambda x: faker.random_element(elements=RunningCategoryEnum.get_names())
    )
    mode = factory.lazy_attribute(
        lambda x: faker.random_element(elements=RunningModeEnum.get_names())
    )
    invite_code = "invite_code"
    status = factory.lazy_attribute(
        lambda x: faker.random_element(elements=RunningStatusEnum.get_names())
    )


class RunningParticipantFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = RunningParticipant

    user_id = factory.lazy_attribute(lambda x: faker.random_int(1, 100000))
    running_id = factory.lazy_attribute(lambda x: faker.random_int(1, 100000))
    status = factory.lazy_attribute(
        lambda x: faker.random_element(elements=RunningParticipantEnum.get_names())
    )


class RunningConfigFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = RunningConfig

    running_id = factory.lazy_attribute(lambda x: faker.random_int(1, 100000))
    category = factory.lazy_attribute(
        lambda x: faker.random_element(elements=RunningConfigCategoryEnum.get_names())
    )
    value = 10


MODEL_FACTORIES = [UserFactory, RunningFactory, RunningParticipantFactory, RunningConfigFactory]
