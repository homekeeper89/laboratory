data = {
    "sample_socket_response": {
        "type": "object",
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
    }
}
