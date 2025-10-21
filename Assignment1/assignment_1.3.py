import redis
from redis.commands.search.field import TextField, NumericField, TagField
from redis.commands.search.index_definition import IndexDefinition, IndexType
from redis.commands.search.query import Query
import json

REDIS_HOST = 'redis-13787.crce220.us-east-1-4.ec2.redns.redis-cloud.com'
REDIS_PORT = 13787
REDIS_PASSWORD = 'Joerex2002!'

# Connect to Redis
print("Connecting to Redis...")
r = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    username='Joerex',
    password=REDIS_PASSWORD,
    decode_responses=True
)

print("Connected to Redis")

def query_laureates_by_category_and_year_range(category, start_year, end_year): #
    """
    Given a category value, return the total number of laureates 
    between a certain year range within the span from year 2013 to year 2023.
    """
    print(f"\nQuerying laureates in category '{category}' from {start_year} to {end_year}.")
    
    # Since year is stored as string/tag, we need to search each year individually
    year_queries = []
    for year in range(start_year, end_year + 1):
        year_queries.append(f"@year:{{{year}}}") #appending the expression for each year
    year_query = "(" + " | ".join(year_queries) + ")" #combining all the year expressions with OR operator and appenidng parentheses
    query_string = f"@category:{{{category}}} {year_query}"
    
    try:
        # Executing  the search for laureates within a certain category and year range
        result = r.ft("idx:year_category_laureates").search(Query(query_string))
        print("result:", result)
        
        # Each documents is a prize with potentially one or multiple laureates
        total_laureates = 0
        for doc in result.docs:
            # Parse the JSON document to count laureates
            prize_data = json.loads(doc.json)
            print(f"Prize Data: {prize_data}")
            if 'laureates' in prize_data:
                total_laureates += len(prize_data['laureates'])
        
        print(f"Total laureates in {category} ({start_year}-{end_year}): {total_laureates}")
        return total_laureates
        
    except Exception as e:
        print(f"Error executing query: {e}")
        return 0


def query_laureates_by_motivation_keyword(keyword):
    """
    Given a keyword, return the total number of laureates that have motivations covering the keyword.
    """
    print(f"\nQuerying laureates with motivation keyword '{keyword}'.")
    
    # Building the search query for motivation field
    query_string = f"@motivation:{keyword}"
    
    try:
        # Execute the search
        result = r.ft("idx:year_category_laureates").search(Query(query_string))
        
        # Count laureates with matching motivations
        total_laureates = 0
        for doc in result.docs:
            prize_data = json.loads(doc.json) #parsing the JSON document for a single prize
            if 'laureates' in prize_data:
                # Counting only laureates whose motivation contains the keyword
                for laureate in prize_data['laureates']:
                    if 'motivation' in laureate and keyword.lower() in laureate['motivation'].lower(): # checking if 'motivation' key exists and contains the keyword
                        total_laureates += 1
        
        print(f"Total laureates with motivation containing '{keyword}': {total_laureates}")
        return total_laureates
        
    except Exception as e:
        print(f"Error executing query: {e}")
        return 0

def query_laureate_by_name(firstname, surname):
    """
    Given the first name and last name, return the year, 
    category and motivation of the laureate.
    """
    print(f"\nQuerying laureate: {firstname} {surname}.")
    
    # Build the search query for both first name and surname
    query_string = f"@firstname:{firstname} @surname:{surname}"
    
    try:
        # Execute the search
        result = r.ft("idx:year_category_laureates").search(Query(query_string))
        
        results = []
        for doc in result.docs:
            prize_data = json.loads(doc.json) #parsing the JSON document for a single prize
            if 'laureates' in prize_data:
                for laureate in prize_data['laureates']: #iterating through the laureates
                    # Checking if this laureate matches the name
                    if (laureate.get('firstname', '').lower() == firstname.lower() and 
                        laureate.get('surname', '').lower() == surname.lower()):
                        
                        result_data = {
                            'year': prize_data.get('year'),
                            'category': prize_data.get('category'),
                            'motivation': laureate.get('motivation')
                        }
                        results.append(result_data)
        
        if results:
            print(f"Found {len(results)} prize(s) for {firstname} {surname}:")
            for i, result_data in enumerate(results, 1):
                print(f"  Prize {i}:")
                print(f"    Year: {result_data['year']}")
                print(f"    Category: {result_data['category']}")
                print(f"    Motivation: {result_data['motivation']}")
        else:
            print(f"No laureate found with name: {firstname} {surname}")
        
        return results
        
    except Exception as e:
        print(f"Error executing query: {e}")
        return []

# Example usage and testing
if __name__ == "__main__":
    
    print("NOBEL PRIZE LAUREATE QUERY SYSTEM")

    
    # Test Query 1: Laureates by category and year range
    #query_laureates_by_category_and_year_range("physics", 2013, 2017)
    
    # Test Query 2: Laureates by motivation keyword
    #query_laureates_by_motivation_keyword("neutrino")
    
    # Test Query 3: Laureate by name
    query_laureate_by_name("Peter", "Higgs")
    
    #print("\n" + "=" * 60)
    print("Query system ready for interactive use!")