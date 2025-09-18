#!/usr/bin/env python3
"""
Quick test script for Discord bot functionality
Run this to test bot functions without Discord
"""

import random
import json
from main import BERRIES, RARITY_WEIGHTS, get_random_berry, get_berry_image_url

def test_berry_system():
    """Test the berry system functions"""
    print("🧪 Testing Berry System...")
    
    # Test random berry generation
    print("\n📊 Testing random berry generation:")
    berry_counts = {}
    for _ in range(100):
        berry = get_random_berry()
        berry_counts[berry] = berry_counts.get(berry, 0) + 1
    
    # Show top 10 most common berries
    sorted_berries = sorted(berry_counts.items(), key=lambda x: x[1], reverse=True)
    print("Top 10 berries from 100 random draws:")
    for berry, count in sorted_berries[:10]:
        rarity = BERRIES[berry]['rarity']
        print(f"  {berry} ({rarity}): {count} times")
    
    # Test image URL generation
    print("\n🖼️ Testing image URL generation:")
    test_berries = ["Oran Berry", "Lum Berry", "Starf Berry"]
    for berry in test_berries:
        url = get_berry_image_url(berry)
        print(f"  {berry}: {url}")
    
    # Test rarity distribution
    print("\n📈 Testing rarity distribution:")
    rarity_counts = {"common": 0, "uncommon": 0, "rare": 0, "legendary": 0}
    for _ in range(1000):
        berry = get_random_berry()
        rarity = BERRIES[berry]['rarity']
        rarity_counts[rarity] += 1
    
    print("Rarity distribution from 1000 draws:")
    for rarity, count in rarity_counts.items():
        percentage = (count / 1000) * 100
        expected_weight = RARITY_WEIGHTS[rarity]
        print(f"  {rarity}: {count} ({percentage:.1f}%) - Expected weight: {expected_weight}")

def test_user_data():
    """Test user data structure"""
    print("\n👤 Testing User Data Structure...")
    
    # Simulate user data
    user_data = {
        '123456789': {
            'inventory': ['Oran Berry', 'Oran Berry', 'Lum Berry', 'Sitrus Berry'],
            'last_daily_claim': '2024-01-01 12:00:00'
        }
    }
    
    user_id = '123456789'
    inventory = user_data[user_id]['inventory']
    
    # Count berries
    berry_counts = {}
    for berry in inventory:
        berry_counts[berry] = berry_counts.get(berry, 0) + 1
    
    print(f"Inventory: {inventory}")
    print(f"Berry counts: {berry_counts}")
    print(f"Total berries: {len(inventory)}")

def test_embed_data():
    """Test embed data generation"""
    print("\n🎨 Testing Embed Data Generation...")
    
    berry_name = "Lum Berry"
    berry_data = BERRIES[berry_name]
    berry_image_url = get_berry_image_url(berry_name)
    
    print(f"Berry: {berry_name}")
    print(f"Emoji: {berry_data['emoji']}")
    print(f"Rarity: {berry_data['rarity']}")
    print(f"Effect: {berry_data['effect']}")
    print(f"Image URL: {berry_image_url}")

if __name__ == "__main__":
    print("🚀 Starting Discord Bot Tests...")
    print("=" * 50)
    
    try:
        test_berry_system()
        test_user_data()
        test_embed_data()
        
        print("\n✅ All tests completed successfully!")
        print("\n💡 Tips for faster Discord testing:")
        print("  1. Use /sync command to force command updates")
        print("  2. Use /debug command to check bot status")
        print("  3. Test in a private DM with your bot")
        print("  4. Use Discord web client (updates faster)")
        print("  5. Check console output for error messages")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
