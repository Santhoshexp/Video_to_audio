"""Module"""
import pika
import json

import pika.spec


def upload(f,fs,channel,access):
    """Method """
    try:
        fid = fs.put(f)
    except Exception as err:
        return "internal error",500
    message = {
        "video_fid": str(fid),
        "mp3_id":None,
        "username":access["username"],
    }
    try:
        channel.basic_publish(
            exchange= "",
            routing_key = 'video',
            body= json.dumps(message),
            properties = pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ),
        )
    except:
        fs.delete(fid)
        return "Internal Server Error",500
    