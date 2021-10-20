from . import db
from datetime import datetime


class Account(db.Model):
    __tablename__ = "accounts"

    id = db.Column(db.Integer, primary_key=True, comment="기본키")
    user_id = db.Column(db.Integer, nullable=False, comment="사용자 기본키")
    category = db.Column(db.String(20), nullable=False, comment="email, kakao, naver,")
    identification = db.Column(db.String(255), nullable=False, comment="신분증")
    password = db.Column(db.String(45), nullable=False, comment="비밀번호")
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, comment="생성된 시간")
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, comment="수정된 시간")


class RunningConfig(db.Model):
    __tablename__ = "running_configs"

    id = db.Column(db.Integer, primary_key=True, comment="기본키")
    running_id = db.Column(db.Integer, nullable=False, comment="달리기 기본키")
    value = db.Column(db.Integer, nullable=False, comment="값")
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, comment="생성된 시간")
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, comment="수정된 시간")


class RunningParticipant(db.Model):
    __tablename__ = "running_participants"

    id = db.Column(db.Integer, primary_key=True, comment="기본키")
    user_id = db.Column(db.Integer, nullable=False, comment="사용자 기본키")
    running_id = db.Column(db.Integer, nullable=False, comment="달리기 기본키")
    status = db.Column(db.String(20), nullable=False, comment="상태")
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, comment="생성된 시간")
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, comment="수정된 시간")


class Running(db.Model):
    __tablename__ = "runnings"

    id = db.Column(db.Integer, primary_key=True, comment="기본키")
    user_id = db.Column(db.Integer, nullable=False, comment="사용자 기본키")
    category = db.Column(
        db.String(20),
        nullable=False,
        server_default="private",
        comment="private, open 으로 구분",
    )
    mode = db.Column(db.String(20), nullable=False, comment="러닝 모드")
    invite_code = db.Column(db.String(10), nullable=False, comment="private 일 경우 필요한 코드")
    status = db.Column(db.String(20), nullable=False, comment="현재 방의 상태")
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, comment="생성된 시간")
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, comment="수정된 시간")


class UserRunningHistory(db.Model):
    __tablename__ = "user_running_histories"

    id = db.Column(db.Integer, primary_key=True, comment="기본키")
    user_id = db.Column(db.Integer, nullable=False, comment="사용자 기본키")
    running_participant_id = db.Column(db.Integer, nullable=False, comment="달리기 참가자 기본키")
    distance = db.Column(db.SmallInteger, nullable=False, comment="거리")
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, comment="생성된 시간")


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, comment="기본키")
    nickname = db.Column(db.String(45), nullable=False, comment="별명")
    status = db.Column(db.String(20), comment="탈퇴: out")
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, comment="생성된 시간")
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, comment="수정된 시간")
