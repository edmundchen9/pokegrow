#!/usr/bin/env python3
"""
Quick test for drop command functionality
"""

from main import get_random_berry, BERRIES, get_berry_image_url

def test_drop_command():
    """Test the drop command logic"""
    print("🎁 Testing Drop Command Logic...")
    print("=" * 40)
    
    # Simulate user data
    user_data = {
        'test_user': {
            'inventory': ['Oran Berry', 'Sitrus Berry', 'Lum Berry'],
            'last_daily_claim': None
        }
    }
    
    user_id = 'test_user'
    
    # Test 1: Initialize user data (like the drop command does)
    if user_id not in user_data:
        user_data[user_id] = {'inventory': [], 'last_daily_claim': None}
    
    if 'inventory' not in user_data[user_id]:
        user_data[user_id]['inventory'] = []
    
    print(f"Initial inventory: {user_data[user_id]['inventory']}")
    
    # Test 2: Get random berry (like drop command does)
    spawned_berry = get_random_berry()
    spawned_berry_data = BERRIES[spawned_berry]
    spawned_image_url = get_berry_image_url(spawned_berry)
    
    print(f"Spawned berry: {spawned_berry}")
    print(f"Berry data: {spawned_berry_data}")
    print(f"Image URL: {spawned_image_url}")
    
    # Test 3: Add to inventory
    user_data[user_id]['inventory'].append(spawned_berry)
    print(f"Updated inventory: {user_data[user_id]['inventory']}")
    
    # Test 4: Create embed data (like drop command does)
    embed_title = "🎁 Berry Spawned!"
    embed_description = f"A **{spawned_berry}** has appeared in your inventory!"
    embed_color = 0x9b59b6
    
    print(f"\nEmbed would show:")
    print(f"Title: {embed_title}")
    print(f"Description: {embed_description}")
    print(f"Color: {hex(embed_color)}")
    print(f"Thumbnail: {spawned_image_url}")
    print(f"Effect: {spawned_berry_data['effect']}")
    print(f"Rarity: {spawned_berry_data['rarity'].title()}")
    print(f"Total berries: {len(user_data[user_id]['inventory'])}")
    
    print("\n✅ Drop command logic test completed!")
    print("If this looks good, the issue is just Discord command sync.")

if __name__ == "__main__":
    test_drop_command()
