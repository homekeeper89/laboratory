from app.domains.running.repository.running_repository import RunningRepository
from app.domains.running.enum import RunningModeEnum


class GetRunningsUseCase:
    # TODO 무한스크롤 형태로 구현
    def __init__(self):
        self.__running_repo = RunningRepository()

    def execute(self, mode: RunningModeEnum, offset: int = 4):
        runnings = self.__running_repo.get_runnings_with_mode(mode, offset)
        if not runnings:
            return {"data": runnings}

        running_list = []
        res = {}
        for record in runnings:
            running = record.Running
            config = record.RunningConfig

            data_set = res.get(running.id, {"meta": {}, "configs": []})
            data_set["configs"].append(
                {
                    "category": config.category,
                    "value": config.value,
                }
            )
            data_set["meta"]["mode"] = running.mode

            res[running.id] = data_set
        running_list.append(res)
        return {"data": running_list, "meta": ""}
