import requests
import settings

def matrix_message(message, prefix='', room='default'):
    # we dont rely on theses, so ignore if it goes wrong
    # TODO at least log that something has gone wrong
    try:
        # login
        details = {
            "type":"m.login.password",
            "user":settings.MATRIX_USER,
            "password":settings.MATRIX_PASSWORD}
        r0 = requests.post(matrix_login_url, json = details)
        access_token = r0.json().get('access_token')

        # join room by id
        url_params = {
            'room': settings.MATRIX_ROOM.get(room),
            'access_token': access_token}
        url = matrix_join_room_id_url.format(**url_params)
        r1 = requests.post(url)

        # send message
        url_params = {
            "room": settings.MATRIX_ROOM.get(room),
            "access_token": access_token}
        url = matrix_send_msg_url.format(**url_params)
        details = {
            "msgtype": "m.text",
            "body": "[%s%s] %s" % (settings.MSG_PREFIX, prefix, message)}
        r2 = requests.post(url, json=details)
        print(r2)
    except Exception as e:
        print(e)
        pass
    return {'result', 'Matrix message sent successfully'}

