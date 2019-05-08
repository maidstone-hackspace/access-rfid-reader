import sys
import requests
import settings

matrix_url = "https://matrix.org/_matrix/client/r0"
matrix_login_url = matrix_url + "/login"
matrix_join_room_alias_url = (
    matrix_url + "/join/{room}?access_token={access_token}"
)
matrix_join_room_id_url = (
    matrix_url + "rooms/%21{room}/join?access_token={access_token}"
)
matrix_send_msg_url = (
    matrix_url
    + "/rooms/%21{room}/send/m.room.message?access_token={access_token}"
)


def matrix_message(message, prefix="", room="default"):
    # we dont rely on theses, so ignore if it goes wrong
    # TODO at least log that something has gone wrong
    try:
        # login
        details = {
            "type": "m.login.password",
            "user": settings.MATRIX_USER,
            "password": settings.MATRIX_PASSWORD,
        }
        r0 = requests.post(matrix_login_url, json=details)
        access_token = r0.json().get("access_token")

        # join room by id
        url_params = {
            "room": settings.MATRIX_ROOM.get(room),
            "access_token": access_token,
        }
        url = matrix_join_room_id_url.format(**url_params)
        r1 = requests.post(url)

        # send message
        url_params = {
            "room": settings.MATRIX_ROOM.get(room),
            "access_token": access_token,
        }
        url = matrix_send_msg_url.format(**url_params)
        details = {
            "msgtype": "m.text",
            "body": "%s%s%s" % (settings.MSG_PREFIX, prefix, message),
        }
        r2 = requests.post(url, json=details)
    except Exception as e:
        ln = sys.exc_info()[-1].tb_lineno
        print(f"{ln} - {e}")
        return
    return {"result", "Matrix message sent successfully"}


if __name__ == "__main__":
    print(settings.MATRIX_ROOM.get('default'))
    matrix_message("test")
