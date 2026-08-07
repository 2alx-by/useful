import jwt
import datetime

secret = "nach Benutzerrechten andere Seiten des ModemManagements aufrufen"

# Create token
token = jwt.encode(
    {
        "sub": "42",
        "name": "Alex",
        "exp": datetime.datetime.now(datetime.timezone.utc)
               + datetime.timedelta(hours=1)
    },
    secret,
    algorithm="HS256"
)

print(token)

# Verify token
payload = jwt.decode(token, secret, algorithms=["HS256"])
print(payload)