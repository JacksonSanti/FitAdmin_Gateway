import redis
import time
import json

def redis_connection():
        
    redis.Redis(
        host='redis',  
        port=6379,        
        db=0,             
        decode_responses=True  
    )


def save_token(email, token, expiration_time):
    redis_client = redis.StrictRedis(host="redis", port=6379, decode_responses=True)

    expiration_timestamp = time.time() + expiration_time
    token_data = {
        "token": token,
        "expiration": expiration_timestamp
    }

    redis_client.set(email, json.dumps(token_data))

    return True


def get_token_by_email(email):

    redis_client = redis.StrictRedis(host="redis", port=6379, decode_responses=True)
    
    token_data = redis_client.get(email) 
    
    if token_data:
        token_data = json.loads(token_data)
        token = token_data["token"]
        expiration = token_data["expiration"]

        if time.time() < expiration:
            return token  
        else:
            redis_client.delete(email)
            return None  
    return None  
