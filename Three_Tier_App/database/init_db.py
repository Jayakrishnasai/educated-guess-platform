import asyncio
import json
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime


async def init_database():
    """Initialize MongoDB database with schema and seed data"""
    
    # Configuration
    MONGODB_URL = "mongodb://localhost:27017"
    DB_NAME = "educated_guess"
    
    # Connect to MongoDB
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client[DB_NAME]
    
    print(f"🔗 Connected to MongoDB: {DB_NAME}")
    
    # Load seed data
    with open('seed_data.json', 'r') as f:
        seed_data = json.load(f)
    
    # Create categories collection and insert data
    print("\n📁 Setting up categories...")
    await db.categories.drop()
    categories = seed_data['categories']
    category_result = await db.categories.insert_many(categories)
    category_map = {cat['slug']: str(id) for cat, id in zip(categories, category_result.inserted_ids)}
    print(f"  ✓ Inserted {len(categories)} categories")
    
    # Create index on slug
    await db.categories.create_index("slug", unique=True)
    print("  ✓ Created unique index on slug")
    
    # Create authors collection and insert data
    print("\n👤 Setting up authors...")
    await db.authors.drop()
    authors = seed_data['authors']
    author_result = await db.authors.insert_many(authors)
    author_map = {author['name']: str(id) for author, id in zip(authors, author_result.inserted_ids)}
    print(f"  ✓ Inserted {len(authors)} authors")
    
    # Create index on name
    await db.authors.create_index("name")
    print("  ✓ Created index on name")
    
    # Create content_items collection and insert data
    print("\n📝 Setting up content items...")
    await db.content_items.drop()
    content_items = []
    for item in seed_data['content_items']:
        content_item = {
            "title": item['title'],
            "description": item['description'],
            "category_id": category_map.get(item['category']),
            "author_id": author_map.get(item['author']),
            "image_url": item['image_url'],
            "tags": item['tags'],
            "created_at": datetime.utcnow()
        }
        content_items.append(content_item)
    
    await db.content_items.insert_many(content_items)
    print(f"  ✓ Inserted {len(content_items)} content items")
    
    # Create indexes
    await db.content_items.create_index([("title", "text"), ("description", "text")])
    await db.content_items.create_index("category_id")
    await db.content_items.create_index([("created_at", -1)])
    print("  ✓ Created indexes (text search, category, created_at)")
    
    # Create users collection with index
    print("\n👥 Setting up users collection...")
    await db.users.drop()
    await db.users.create_index("email", unique=True)
    print("  ✓ Created unique index on email")
    
    print("\n✅ Database initialization complete!")
    print(f"\n📊 Summary:")
    print(f"  - {await db.categories.count_documents({})} categories")
    print(f"  - {await db.authors.count_documents({})} authors")
    print(f"  - {await db.content_items.count_documents({})} content items")
    print(f"  - Users collection ready")
    
    # Close connection
    client.close()


if __name__ == "__main__":
    asyncio.run(init_database())
