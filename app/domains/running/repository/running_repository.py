from app.core.database import session
from app.core.database.models import Running


class RunningRepository:
    def create_running(self, user_id: int, category: str, mode: str, invite_code: str, status: str):
        try:
            session.add(
                Running(
                    user_id=user_id,
                    category=category,
                    mode=mode,
                    invite_code=invite_code,
                    status=status,
                )
            )
            session.commit()
            res = True
        except Exception as e:
            session.rollback()
            session.flush()
            print(e)
            res = False

        return res
