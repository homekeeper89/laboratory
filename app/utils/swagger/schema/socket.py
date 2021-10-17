data = {
    "connect":{
        "type": "object",
        "description":"socket에 접속한다",
        "properties": {
            "status": {"type": "integer", "description": "해당 소켓 이벤트에 대한 성공 여부, http status code 와 우선은 동일하게 진행"},
            "data": {
                "type": "object",
            },
            "meta": {
                "type": "object",
            },
        },
    },
    "disconnect":{
        "type": "object",
        "description":"socket에 접속을 종료한다",
        "properties": {
            "status": {"type": "integer", "description": "해당 소켓 이벤트에 대한 성공 여부, http status code 와 우선은 동일하게 진행"},
            "data": {
                "type": "object",
            },
            "meta": {
                "type": "object",
            },
        },
    },
    "send_gps_data": {
        "type": "object",
        "description":"이전 위경도 + 현재 위경도를 바탕으로 이동한 거리를 계산하여 내려준다",
        "properties": {
            "status": {"type": "integer", "description": "해당 소켓 이벤트에 대한 성공 여부, http status code 와 우선은 동일하게 진행"},
            "data": {
                "type": "object",
                "properties": {
                    "distance": {"type": "integer", "description": "계산된 거리, 총 거리가 아님"},
                    "user_id": {"type": "string"},
                },
            },
            "meta": {
                "type": "object",
                "properties": {
                    "message": {"type": "string", "description": "상태 메세지에 대한 설명, 200인 경우 없음"},
                },
            },
        },
    },
    "join_room":{
        "type": "object",
        "description":"socket-room 을 접속한다",
        "properties": {
            "status": {"type": "integer", "description": "해당 소켓 이벤트에 대한 성공 여부, http status code 와 우선은 동일하게 진행"},
            "data": {
                "type": "object",
            },
            "meta": {
                "type": "object",
            },
        },
    },
    "leave_room":{
        "type": "object",
        "description":"접속해있는 room을 떠난다.",
        "properties": {
            "status": {"type": "integer", "description": "해당 소켓 이벤트에 대한 성공 여부, http status code 와 우선은 동일하게 진행"},
            "data": {
                "type": "object",
            },
            "meta": {
                "type": "object",
            },
        },
    }
}
