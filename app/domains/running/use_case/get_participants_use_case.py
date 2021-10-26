from typing import Optional
import uuid
from app.domains.running.dto import CreateRunningData, RunningConfigData
from app.domains.running.enum import RunningCategoryEnum, RunningModeEnum, RunningStatusEnum
from app.domains.running.repository.running_repository import RunningRepository
from app.core.exceptions import FailUseCaseLogicException


class GetParticipantsUseCase:
    def __init__(self):
        self.__running_repo = RunningRepository()

    def execute(self, running_id: int, user_id: int):
        return {"data": [{}, {}, {}, {}, {}]}
