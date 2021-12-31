from app.base.request import BaseRequestModel
from pydantic import Field, validator
from app.domains.running.enum import RunningCategoryEnum, RunningModeEnum


class CreateParticipationRequestSchema(BaseRequestModel):
    running_id: int = None
    invite_code: str = Field(None, title="비공개방 초대 코드", description="비공개방 참여시 필요한 코드, 방 생성때 만들어짐")


class GetRunningsRequestSchema(BaseRequestModel):
    mode: RunningModeEnum = Field(None, title="Running Mode", description="러닝 모드에 대한")
    offset: int = Field(3, description="목록 가져올 갯수")

    @validator("mode", pre=True)
    def _validate_mode(cls, value: str):
        if not RunningModeEnum.has_value(value):
            raise ValueError(f"invalid_mode: {value}")
        return value.upper()


class RunningConfingSchema(BaseRequestModel):
    distance: int = Field(500, description="단위:m, 달리기 생성시 달릴거리")
    limit_minutes: int = Field(10, description="단위:m, 같이 달릴 총 시간")
    limit_user_counts: int = Field(4, description="인원 제한")


class CreateRunningSchema(BaseRequestModel):
    user_id: int = Field(None)
    category: RunningCategoryEnum = Field(
        RunningCategoryEnum.PRIVATE, description="러닝 생성시 종류, 공개 여부를 결정한다"
    )
    mode: RunningModeEnum = Field(RunningModeEnum.COMPETITION, description="러닝 생성시 모드")
    config: RunningConfingSchema = Field(None, description="러닝 생성시 필요한 설정 값들")

    @validator("category", "mode", pre=True)
    def _validate_fields(cls, value):
        return value.upper()

    @validator("config", pre=True, always=True)
    def _validate_config(cls, value: dict = None):
        if not value:
            return RunningConfingSchema()
        return RunningConfingSchema(**value)
