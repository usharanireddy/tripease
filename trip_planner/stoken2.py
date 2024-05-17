from itsdangerous import URLSafeTimedSerializer
from key import secret_key
def token2(data2,salt):
    serializer= URLSafeTimedSerializer(secret_key)
    return serializer.dumps(data2,salt=salt)