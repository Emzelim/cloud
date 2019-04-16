"""
1. Génére un objet JSON de toutes les variables Redis
2a. Envoie toutes les variables de Redis à Télégraf
2b. Attend qu'il y'ai un changement (event 'set') sur une variable Redis pour
    renvoyer uniquement cette variable à Télégraf

Note :
    - Un champ supplémentaire dans les valeurs envoyé pour préciser de quel robot ça provient.
    - Un JSON global est créer afin de ne pas envoyer des valeurs null (pose problème si valeur null)
"""
import redis
import aioredis
from telegraf.client import TelegrafClient
import asyncio
import json
import time

REDIS_URI = 'redis://localhost:6379'
REDIS_HOST = '127.0.0.1'

TELEGRAF_HOST = '127.0.0.1'
TELEGRAF_PORT = 8092

MEASUREMENT_NAME = 'local_test7'
Armin_ID = 18587
Armin_ID_COL = 'Armin_ID'


async def main_loop1(redis_client, telegraf_client, json_data):

    channel = '__keyevent@0__:set'

    sub_redis = await aioredis.create_redis(REDIS_URI)

    try:
        # ---- Send value only on change
        subscription = await sub_redis.subscribe(channel)
        print('subscription', subscription)
        channel = subscription[0]
        while await channel.wait_message():
            key = await channel.get()

            value = format_value(key, redis_client.get(key))
            key_name = str(key)[2:-1]

            json_data[key_name] = value

            telegraf_client.metric(MEASUREMENT_NAME, json_data)

            print("Change: {} to {}".format(key_name, json_data[key_name]))
    finally:
        sub_redis.close()
        await sub_redis.wait_closed()


async def main_loop2(redis_client, telegraf_client, json_data):
    # ---- Send all values
    while True:
        await asyncio.sleep(5)
        for key in redis_client.scan_iter('plc:*'):
            value = str(redis_client.get(key))
            key_name = str(key)
            json_data[key_name] = value

        telegraf_client.metric(MEASUREMENT_NAME, json_data)
        print('all data sended')


def get_json_data(redis_client):
    # ---- Send all values
    print('Generating : json_data')
    json_string = '{'
    for key in redis_client.scan_iter('plc:*'):
        value = str(redis_client.get(key))
        key_name = str(key)

        json_string += '"' + key_name + '": ' + value + ', '

        print("Initialisation: {} : {}".format(key_name, value))

    json_string += '"' + Armin_ID_COL + '": ' + str(Armin_ID) + '}'

    print('Generated : json_data')

    return json.loads(json_string)


def format_value(key, value):
    # --- Formatting value
    if str(key).startswith("b'plc:i_") or str(key).startswith("b'plc:u_"):
        return int(value)
    elif str(key).startswith("b'plc:b_"):
        return str_boolean(value)
    elif str(key).startswith("b'plc:r_"):
        return float(value)


def str_boolean(string):
    if string == "false":
        return False
    else:
        return True


if __name__ == "__main__":
    print("###### BEFORE RUN ######")

    # Connect to Redis
    print("Connecting to Redis...")
    redis_cli = redis.StrictRedis(host=REDIS_HOST, decode_responses=True)
    print("Redis connected.")

    # Connect to Telegraf
    print("Connecting to Telegraf")
    telegraf_cli = TelegrafClient(host=TELEGRAF_HOST, port=TELEGRAF_PORT)
    print("Telegrag is connected")

    json_all_data = get_json_data(redis_cli)

    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(asyncio.gather(
        main_loop1(redis_cli, telegraf_cli, json_all_data),
        main_loop2(redis_cli, telegraf_cli, json_all_data),

    ))
    event_loop.close()
    event_loop.run_forever()
    print("###### AFTER RUN ######")
