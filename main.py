import os
import discord
from dotenv import load_dotenv
import logging
from discord.ext import commands
import random
import json


load_dotenv()

token = os.getenv('DISCORD_TOKEN')

# Berry data based on Serebii.net berry list
BERRIES = {
    "Oran Berry": {"emoji": "🫐", "rarity": "common", "effect": "Restores HP when held", "image": "https://www.serebii.net/itemdex/sprites/oranberry.png"},
    "Sitrus Berry": {"emoji": "🍊", "rarity": "common", "effect": "Restores more HP when held", "image": "https://www.serebii.net/itemdex/sprites/sitrusberry.png"},
    "Pecha Berry": {"emoji": "🍑", "rarity": "common", "effect": "Cures poison when held"},
    "Rawst Berry": {"emoji": "🍓", "rarity": "common", "effect": "Cures burn when held"},
    "Chesto Berry": {"emoji": "🌰", "rarity": "common", "effect": "Cures sleep when held"},
    "Aspear Berry": {"emoji": "🍐", "rarity": "common", "effect": "Cures freeze when held"},
    "Persim Berry": {"emoji": "🥭", "rarity": "common", "effect": "Cures confusion when held"},
    "Cheri Berry": {"emoji": "🍒", "rarity": "common", "effect": "Cures paralysis when held"},
    "Leppa Berry": {"emoji": "🍎", "rarity": "uncommon", "effect": "Restores 10 PP when held"},
    "Lum Berry": {"emoji": "💎", "rarity": "rare", "effect": "Cures any status condition when held"},
    "Aguav Berry": {"emoji": "🥝", "rarity": "uncommon", "effect": "Restores HP in pinch, confuses if disliked"},
    "Figy Berry": {"emoji": "🍇", "rarity": "uncommon", "effect": "Restores HP in pinch, confuses if disliked"},
    "Iapapa Berry": {"emoji": "🍌", "rarity": "uncommon", "effect": "Restores HP in pinch, confuses if disliked"},
    "Mago Berry": {"emoji": "🍅", "rarity": "uncommon", "effect": "Restores HP in pinch, confuses if disliked"},
    "Wiki Berry": {"emoji": "🥥", "rarity": "uncommon", "effect": "Restores HP in pinch, confuses if disliked"},
    "Apicot Berry": {"emoji": "🥭", "rarity": "rare", "effect": "Boosts Sp. Def in pinch"},
    "Ganlon Berry": {"emoji": "🍈", "rarity": "rare", "effect": "Boosts Defense in pinch"},
    "Lansat Berry": {"emoji": "🍋", "rarity": "rare", "effect": "Boosts critical hit ratio in pinch"},
    "Liechi Berry": {"emoji": "🍄", "rarity": "rare", "effect": "Boosts Attack in pinch"},
    "Petaya Berry": {"emoji": "🍆", "rarity": "rare", "effect": "Boosts Sp. Atk in pinch"},
    "Salac Berry": {"emoji": "🥒", "rarity": "rare", "effect": "Boosts Speed in pinch"},
    "Starf Berry": {"emoji": "⭐", "rarity": "legendary", "effect": "Sharply boosts random stat in pinch"},
    "Enigma Berry": {"emoji": "❓", "rarity": "legendary", "effect": "Restores HP when hit by super-effective move"},
    "Micle Berry": {"emoji": "💫", "rarity": "legendary", "effect": "Boosts accuracy of next move in pinch"},
    "Custap Berry": {"emoji": "⚡", "rarity": "legendary", "effect": "Goes first in pinch"},
    "Jaboca Berry": {"emoji": "🥜", "rarity": "rare", "effect": "Damages attacker when hit by physical move"},
    "Rowap Berry": {"emoji": "🌰", "rarity": "rare", "effect": "Damages attacker when hit by special move"},
    "Kee Berry": {"emoji": "🍯", "rarity": "rare", "effect": "Boosts Defense when hit by physical move"},
    "Maranga Berry": {"emoji": "🥥", "rarity": "rare", "effect": "Boosts Sp. Def when hit by special move"},
    "Razz Berry": {"emoji": "🍓", "rarity": "common", "effect": "Used for Pokéblocks - enhances Coolness"},
    "Bluk Berry": {"emoji": "🫐", "rarity": "common", "effect": "Used for Pokéblocks - enhances Beauty"},
    "Nanab Berry": {"emoji": "🍌", "rarity": "common", "effect": "Used for Pokéblocks - enhances Cuteness"},
    "Wepear Berry": {"emoji": "🍐", "rarity": "common", "effect": "Used for Pokéblocks - enhances Cleverness"},
    "Pinap Berry": {"emoji": "🍍", "rarity": "common", "effect": "Used for Pokéblocks - enhances Toughness"},
    "Pomeg Berry": {"emoji": "🍎", "rarity": "uncommon", "effect": "Increases friendship, decreases HP EVs"},
    "Kelpsy Berry": {"emoji": "🥬", "rarity": "uncommon", "effect": "Increases friendship, decreases Attack EVs"},
    "Qualot Berry": {"emoji": "🍊", "rarity": "uncommon", "effect": "Increases friendship, decreases Defense EVs"},
    "Hondew Berry": {"emoji": "🍈", "rarity": "uncommon", "effect": "Increases friendship, decreases Sp. Atk EVs"},
    "Grepa Berry": {"emoji": "🍇", "rarity": "uncommon", "effect": "Increases friendship, decreases Sp. Def EVs"},
    "Tamato Berry": {"emoji": "🍅", "rarity": "uncommon", "effect": "Increases friendship, decreases Speed EVs"},
    "Cornn Berry": {"emoji": "🌽", "rarity": "rare", "effect": "Used for Pokéblocks - enhances Beauty"},
    "Magost Berry": {"emoji": "🥭", "rarity": "rare", "effect": "Used for Pokéblocks - enhances Cuteness"},
    "Rabuta Berry": {"emoji": "🍇", "rarity": "rare", "effect": "Used for Pokéblocks - enhances Cleverness"},
    "Nomel Berry": {"emoji": "🍋", "rarity": "rare", "effect": "Used for Pokéblocks - enhances Toughness"},
    "Spelon Berry": {"emoji": "🍅", "rarity": "rare", "effect": "Used for Pokéblocks - enhances Cuteness"},
    "Pamtre Berry": {"emoji": "🍑", "rarity": "rare", "effect": "Used for Pokéblocks - enhances Beauty"},
    "Watmel Berry": {"emoji": "🍉", "rarity": "rare", "effect": "Used for Pokéblocks - enhances Cleverness"},
    "Durin Berry": {"emoji": "🥒", "rarity": "rare", "effect": "Used for Pokéblocks - enhances Toughness"},
    "Belue Berry": {"emoji": "🍇", "rarity": "rare", "effect": "Used for Pokéblocks - enhances Beauty"},
    "Chople Berry": {"emoji": "🌶️", "rarity": "uncommon", "effect": "Weakens super-effective Fighting moves"},
    "Kebia Berry": {"emoji": "🍃", "rarity": "uncommon", "effect": "Weakens super-effective Poison moves"},
    "Shuca Berry": {"emoji": "🥜", "rarity": "uncommon", "effect": "Weakens super-effective Ground moves"},
    "Coba Berry": {"emoji": "🪶", "rarity": "uncommon", "effect": "Weakens super-effective Flying moves"},
    "Payapa Berry": {"emoji": "🧠", "rarity": "uncommon", "effect": "Weakens super-effective Psychic moves"},
    "Tanga Berry": {"emoji": "🐛", "rarity": "uncommon", "effect": "Weakens super-effective Bug moves"},
    "Charti Berry": {"emoji": "🪨", "rarity": "uncommon", "effect": "Weakens super-effective Rock moves"},
    "Kasib Berry": {"emoji": "👻", "rarity": "uncommon", "effect": "Weakens super-effective Ghost moves"},
    "Haban Berry": {"emoji": "🐉", "rarity": "uncommon", "effect": "Weakens super-effective Dragon moves"},
    "Colbur Berry": {"emoji": "🌑", "rarity": "uncommon", "effect": "Weakens super-effective Dark moves"},
    "Babiri Berry": {"emoji": "⚙️", "rarity": "uncommon", "effect": "Weakens super-effective Steel moves"},
    "Chilan Berry": {"emoji": "🥊", "rarity": "uncommon", "effect": "Weakens super-effective Normal moves"},
    "Occa Berry": {"emoji": "🔥", "rarity": "uncommon", "effect": "Weakens super-effective Fire moves"},
    "Passho Berry": {"emoji": "💧", "rarity": "uncommon", "effect": "Weakens super-effective Water moves"},
    "Wacan Berry": {"emoji": "⚡", "rarity": "uncommon", "effect": "Weakens super-effective Electric moves"},
    "Rindo Berry": {"emoji": "🌱", "rarity": "uncommon", "effect": "Weakens super-effective Grass moves"},
    "Yache Berry": {"emoji": "❄️", "rarity": "uncommon", "effect": "Weakens super-effective Ice moves"},
    "Roseli Berry": {"emoji": "🌸", "rarity": "uncommon", "effect": "Weakens super-effective Fairy moves"}
}

# Rarity weights for random selection
RARITY_WEIGHTS = {
    "common": 50,
    "uncommon": 30,
    "rare": 15,
    "legendary": 5
}

# User data storage (in a real bot, you'd use a database)
user_data = {}

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.messages = True

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user.name} is ready!")
    # Sync slash commands with Discord
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} slash commands")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

def get_berry_image_url(berry_name):
    """Generate Serebii.net image URL for a berry"""
    # Convert berry name to Serebii format (lowercase, no spaces)
    berry_id = berry_name.lower().replace(" ", "").replace("berry", "berry")
    return f"https://www.serebii.net/itemdex/sprites/{berry_id}.png"

def get_random_berry():
    """Get a random berry based on rarity weights"""
    # Create weighted list based on rarity
    weighted_berries = []
    for berry_name, berry_data in BERRIES.items():
        weight = RARITY_WEIGHTS[berry_data["rarity"]]
        weighted_berries.extend([berry_name] * weight)
    
    return random.choice(weighted_berries)

def can_claim_daily(user_id):
    """Check if user can claim daily reward"""
    import datetime
    now = datetime.datetime.now()
    last_claim = user_data.get(user_id, {}).get('last_daily_claim')
    
    if not last_claim:
        return True
    
    # Check if 24 hours have passed
    time_diff = now - last_claim
    return time_diff.total_seconds() >= 86400  # 24 hours in seconds

def claim_daily(user_id):
    """Mark user as having claimed daily reward"""
    import datetime
    if user_id not in user_data:
        user_data[user_id] = {'inventory': [], 'last_daily_claim': None}
    
    user_data[user_id]['last_daily_claim'] = datetime.datetime.now()
    
    # Add berry to inventory
    berry = get_random_berry()
    if 'inventory' not in user_data[user_id]:
        user_data[user_id]['inventory'] = []
    user_data[user_id]['inventory'].append(berry)
    
    return berry

@bot.tree.command(name='daily', description='Claim your daily berry reward!')
async def daily_command(interaction: discord.Interaction):
    """Claim your daily berry reward!"""
    user_id = str(interaction.user.id)
    
    if not can_claim_daily(user_id):
        import datetime
        last_claim = user_data[user_id]['last_daily_claim']
        next_claim = last_claim + datetime.timedelta(hours=24)
        time_left = next_claim - datetime.datetime.now()
        
        hours = int(time_left.total_seconds() // 3600)
        minutes = int((time_left.total_seconds() % 3600) // 60)
        
        await interaction.response.send_message(f"⏰ You've already claimed your daily berry! Come back in {hours}h {minutes}m")
        return
    
    # Claim daily reward
    berry_name = claim_daily(user_id)
    berry_data = BERRIES[berry_name]
    
    # Create embed for nice display
    embed = discord.Embed(
        title="🌱 Daily Berry Reward!",
        description=f"You received a **{berry_name}** {berry_data['emoji']}",
        color=0x00ff00
    )
    
    # Add berry image
    berry_image_url = get_berry_image_url(berry_name)
    embed.set_thumbnail(url=berry_image_url)
    
    embed.add_field(
        name="Effect",
        value=berry_data['effect'],
        inline=False
    )
    
    embed.add_field(
        name="Rarity",
        value=berry_data['rarity'].title(),
        inline=True
    )
    
    embed.add_field(
        name="Inventory",
        value=f"You now have {len(user_data[user_id]['inventory'])} berries!",
        inline=True
    )
    
    embed.set_footer(text="Come back tomorrow for another berry!")
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name='inventory', description='Check your berry inventory')
async def inventory_command(interaction: discord.Interaction):
    """Check your berry inventory"""
    user_id = str(interaction.user.id)
    
    if user_id not in user_data or not user_data[user_id].get('inventory'):
        await interaction.response.send_message("📦 Your inventory is empty! Use `/daily` to get your first berry!")
        return
    
    inventory = user_data[user_id]['inventory']
    
    # Count berries
    berry_counts = {}
    for berry in inventory:
        berry_counts[berry] = berry_counts.get(berry, 0) + 1
    
    # Create embed
    embed = discord.Embed(
        title=f"📦 {ctx.author.display_name}'s Berry Inventory",
        description=f"Total berries: {len(inventory)}",
        color=0x00ff00
    )
    
    # Add berries to embed (limit to 25 fields due to Discord limits)
    for i, (berry_name, count) in enumerate(list(berry_counts.items())[:25]):
        berry_data = BERRIES[berry_name]
        embed.add_field(
            name=f"{berry_data['emoji']} {berry_name}",
            value=f"x{count} - {berry_data['rarity'].title()}",
            inline=True
        )
    
    if len(berry_counts) > 25:
        embed.add_field(
            name="...",
            value=f"and {len(berry_counts) - 25} more berries",
            inline=False
        )
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name='berry', description='Get detailed information about a specific berry')
async def berry_info_command(interaction: discord.Interaction, berry_name: str):
    """Get detailed information about a specific berry"""
    if not berry_name:
        await interaction.response.send_message("Please specify a berry name! Example: `/berry Oran Berry`")
        return
    
    # Find berry (case insensitive)
    berry_found = None
    for berry_key in BERRIES.keys():
        if berry_name.lower() in berry_key.lower():
            berry_found = berry_key
            break
    
    if not berry_found:
        await interaction.response.send_message(f"Berry '{berry_name}' not found! Use `/inventory` to see available berries.")
        return
    
    berry_data = BERRIES[berry_found]
    berry_image_url = get_berry_image_url(berry_found)
    
    # Create detailed embed
    embed = discord.Embed(
        title=f"{berry_data['emoji']} {berry_found}",
        description=berry_data['effect'],
        color=0x00ff00
    )
    
    # Add berry image
    embed.set_thumbnail(url=berry_image_url)
    
    embed.add_field(
        name="Rarity",
        value=berry_data['rarity'].title(),
        inline=True
    )
    
    embed.add_field(
        name="Type",
        value="Berry",
        inline=True
    )
    
    embed.add_field(
        name="Source",
        value="Serebii.net",
        inline=True
    )
    
    embed.set_footer(text="Data from Serebii.net ItemDex")
    
    await interaction.response.send_message(embed=embed)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if "meow" in message.content.lower():
        await message.channel.send("Meow! 🐱")
    
    await bot.process_commands(message)

bot.run(token)