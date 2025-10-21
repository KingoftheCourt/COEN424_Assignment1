import redis
import json
import requests

REDIS_HOST = 'redis-13787.crce220.us-east-1-4.ec2.redns.redis-cloud.com' # Redis host details
REDIS_PORT = 13787  # Redis port number
REDIS_PASSWORD = 'Joerex2002!'  # Redis password


# Testing Redis Connections
print("Testing Redis connection")
try:
    r = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        password=REDIS_PASSWORD,
        username='Joerex',
        decode_responses=True
    )
    r.ping()
    print("Successfully connected to Redis!")
except Exception as e:
    print(f"Connection failed: {e}")
    exit()

# Fetch Nobel Prize data from the https link
print("\nFetching Nobel Prize data.")
response = requests.get('https://api.nobelprize.org/v1/prize.json')
data = response.json()
print(f"Fetched {len(data['prizes'])} total prizes")

# Loading prizes from 2013-2023
print("\nLoading prizes from 2013-2023")
prize_count = 1
for prize in data['prizes']:
    year = int(prize['year'])
    if 2013 <= year <= 2023:
        key = f"prizes:{prize_count}"
        r.json().set(key, '$', prize)
        print(f"  Loaded: {year} - {prize['category']}")
        prize_count += 1

print(f"\n Total prizes loaded: {prize_count - 1}")