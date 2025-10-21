import redis
from redis.commands.search.field import TextField, NumericField, TagField
#from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.index_definition import IndexDefinition, IndexType


REDIS_HOST = 'redis-13787.crce220.us-east-1-4.ec2.redns.redis-cloud.com' # Redis host details
REDIS_PORT = 13787  # Redis port number
REDIS_PASSWORD = 'Joerex2002!'  # Redis password


# Connecting  to Redis
print("Connecting to Redis...")
r = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    username='Joerex',
    password=REDIS_PASSWORD,
    decode_responses=True
)

print("Connected to Redis!")

# Drop existing index first to recreate it
print("\nDropping existing index if it exists...")
try:
    r.ft("idx:year_category_laureates").dropindex()
    print("Existing index dropped")
except Exception as e:
    print(f"No existing index to drop: {e}")

# Creating  the index 
print("\nCreating index 'idx:year_category_laureates.")
try:
    # Definining the schema for the index
    schema = [
        # Indexing year as a tag field since it's stored as string
        TagField("$.year", as_name="year"),
        
        # Indexing cateogry as a tag field to obtain exact matches
        TagField("$.category", as_name="category"),
        
        # Indexing laureate first names (searchable text)
        TextField("$.laureates[*].firstname", as_name="firstname"),
        
        # Indexing laureate surnames (searchable text)
        TextField("$.laureates[*].surname", as_name="surname"),
        
        # Indexing laureate motivations (searchable text for keywords)
        TextField("$.laureates[*].motivation", as_name="motivation")
    ]
    
    # Create the index
    r.ft("idx:year_category_laureates").create_index(
        schema,
        definition=IndexDefinition(
            prefix=["prizes:"],  # Index all keys starting with "prizes:"
            index_type=IndexType.JSON  # We're indexing JSON data
        )
    )

    print("Index 'idx:year_category_laureates' created successfully!")

except Exception as e:
    if "Index already exists" in str(e):
        print(" Index already exists")
    else:
        print(f"Error creating index: {e}")

