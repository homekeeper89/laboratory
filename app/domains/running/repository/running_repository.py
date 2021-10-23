from app.core.database import session
from app.core.database.models import Running


class RunningRepository:
    def create_running(
        self, user_id: int, category: str, mode: str, invite_code: str, status: str
    ) -> int:
        try:
            model = Running(
                user_id=user_id,
                category=category,
                mode=mode,
                invite_code=invite_code,
                status=status,
            )
            session.add(model)
            session.commit()
            session.refresh(model)

            return model.id
        except Exception as e:
            session.rollback()
            session.flush()
            print(e)
            return 0
