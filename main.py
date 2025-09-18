import os
import discord
from dotenv import load_dotenv
import logging
from discord.ext import commands
import random
import json
import asyncio


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

# Additional items beyond berries
ITEMS = {
    "Rare Candy": {"emoji": "🍭", "rarity": "legendary", "effect": "Raises a Pokémon's level by 1", "type": "item"},
}

# Rarity weights for random selection
RARITY_WEIGHTS = {
    "common": 60,
    "uncommon": 24,
    "rare": 15,
    "legendary": 1
}

# User data storage (in a real bot, you'd use a database)
user_data = {}

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user.name} is ready!")
    print(f"Bot ID: {bot.user.id}")
    print(f"Connected to {len(bot.guilds)} servers")
    
    # Sync slash commands with Discord
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} slash commands")
        for cmd in synced:
            print(f"  - {cmd.name}")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

@bot.tree.command(name='sync', description='Sync slash commands to this server')
async def sync_commands(interaction: discord.Interaction):
    """Sync slash commands to this server"""
    # Check if user has permission (optional - you can remove this check)
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ You need Administrator permissions to sync commands!", ephemeral=True)
        return
    
    try:
        # Send initial response
        await interaction.response.send_message("🔄 Syncing commands...", ephemeral=True)
        
        # Sync commands
        synced = await bot.tree.sync()
        
        # Send success message
        await interaction.followup.send(f"✅ Successfully synced {len(synced)} slash commands to this server!", ephemeral=True)
        
        # List the synced commands
        command_list = "\n".join([f"• `/{cmd.name}`" for cmd in synced])
        await interaction.followup.send(f"**Synced Commands:**\n{command_list}", ephemeral=True)
        
    except discord.app_commands.CommandSyncFailure as e:
        await interaction.followup.send(f"❌ Command sync failed: {e}", ephemeral=True)
    except Exception as e:
        await interaction.followup.send(f"❌ Unexpected error during sync: {str(e)}", ephemeral=True)
        print(f"Sync error: {e}")  # Log to console for debugging

def get_item_image_url(item_name):
    """Generate Serebii.net image URL for any item"""
    # Convert item name to Serebii format (lowercase, no spaces)
    item_id = item_name.lower().replace(" ", "")
    return f"https://www.serebii.net/itemdex/sprites/{item_id}.png"

def get_berry_image_url(berry_name):
    """Generate Serebii.net image URL for a berry (backward compatibility)"""
    return get_item_image_url(berry_name)

def get_random_item():
    """Get a random item (berry or other item) based on rarity weights"""
    # Combine berries and items
    all_items = {**BERRIES, **ITEMS}
    
    # Create weighted list based on rarity
    weighted_items = []
    for item_name, item_data in all_items.items():
        weight = RARITY_WEIGHTS[item_data["rarity"]]
        weighted_items.extend([item_name] * weight)
    
    return random.choice(weighted_items)

def get_random_berry():
    """Get a random berry based on rarity weights (backward compatibility)"""
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
        description=f"You received a **{berry_name}**",
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
    
    # If user has only a few berries, show detailed embeds with images
    if len(berry_counts) <= 5:
        embeds = []
        for berry_name, count in berry_counts.items():
            berry_data = BERRIES[berry_name]
            berry_image_url = get_berry_image_url(berry_name)
            
            embed = discord.Embed(
                title=f"{berry_name}",
                description=f"**Quantity:** x{count}\n**Rarity:** {berry_data['rarity'].title()}\n**Effect:** {berry_data['effect']}",
                color=0x00ff00
            )
            embed.set_thumbnail(url=berry_image_url)
            embeds.append(embed)
        
        await interaction.response.send_message(embeds=embeds)
        return
    
    # For larger inventories, show compact list with first berry as main image
    embed = discord.Embed(
        title=f"📦 {interaction.user.display_name}'s Berry Inventory",
        description=f"Total berries: {len(inventory)}",
        color=0x00ff00
    )
    
    # Set the first berry as the main image
    first_berry = list(berry_counts.keys())[0]
    first_berry_image = get_berry_image_url(first_berry)
    embed.set_thumbnail(url=first_berry_image)
    
    # Add berries to embed (limit to 25 fields due to Discord limits)
    for i, (berry_name, count) in enumerate(list(berry_counts.items())[:25]):
        berry_data = BERRIES[berry_name]
        embed.add_field(
            name=f"{berry_name}",
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
        title=f"{berry_found}",
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

@bot.tree.command(name='drop', description='Spawn a random berry into your inventory')
async def drop_command(interaction: discord.Interaction):
    """Spawn a random berry into your inventory"""
    user_id = str(interaction.user.id)
    
    # Initialize user data if needed
    if user_id not in user_data:
        user_data[user_id] = {'inventory': [], 'last_daily_claim': None}
    
    if 'inventory' not in user_data[user_id]:
        user_data[user_id]['inventory'] = []
    
    # Get a random item (berry or other item)
    spawned_item = get_random_item()
    
    # Check if it's a berry or other item
    if spawned_item in BERRIES:
        spawned_item_data = BERRIES[spawned_item]
        item_type = "Berry"
        embed_title = "🍓 Berry Spawned!"
    else:
        spawned_item_data = ITEMS[spawned_item]
        item_type = "Item"
        embed_title = "🎁 Item Spawned!"
    
    spawned_image_url = get_item_image_url(spawned_item)
    
    # Add item to inventory
    user_data[user_id]['inventory'].append(spawned_item)
    
    # Create embed for spawn notification
    embed = discord.Embed(
        title=embed_title,
        description=f"A **{spawned_item}** has appeared in your inventory!",
        color=0x9b59b6
    )
    
    # Add item image
    embed.set_thumbnail(url=spawned_image_url)
    
    embed.add_field(
        name="Effect",
        value=spawned_item_data['effect'],
        inline=False
    )
    
    embed.add_field(
        name="Rarity",
        value=spawned_item_data['rarity'].title(),
        inline=True
    )
    
    embed.add_field(
        name="Type",
        value=item_type,
        inline=True
    )
    
    embed.add_field(
        name="Inventory Total",
        value=f"{len(user_data[user_id]['inventory'])} items",
        inline=True
    )
    
    # TODO: Add 10 minute cooldown for live implementation
    # embed.set_footer(text="⏰ Next spawn available in 10 minutes")
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name='debug', description='Debug information about the bot')
async def debug_command(interaction: discord.Interaction):
    """Debug information about the bot"""
    user_id = str(interaction.user.id)
    
    # Get user data
    user_inventory = user_data.get(user_id, {}).get('inventory', [])
    user_daily_claim = user_data.get(user_id, {}).get('last_daily_claim')
    
    # Create debug embed
    embed = discord.Embed(
        title="🔧 Debug Information",
        color=0x3498db
    )
    
    embed.add_field(
        name="User ID",
        value=user_id,
        inline=True
    )
    
    embed.add_field(
        name="Inventory Count",
        value=len(user_inventory),
        inline=True
    )
    
    embed.add_field(
        name="Last Daily Claim",
        value=str(user_daily_claim) if user_daily_claim else "Never",
        inline=True
    )
    
    embed.add_field(
        name="Bot Latency",
        value=f"{round(bot.latency * 1000)}ms",
        inline=True
    )
    
    embed.add_field(
        name="Server Count",
        value=len(bot.guilds),
        inline=True
    )
    
    embed.add_field(
        name="Command Count",
        value=len(bot.tree.get_commands()),
        inline=True
    )
    
    # Show first few berries in inventory
    if user_inventory:
        inventory_preview = ", ".join(user_inventory[:5])
        if len(user_inventory) > 5:
            inventory_preview += f" ... (+{len(user_inventory) - 5} more)"
        embed.add_field(
            name="Inventory Preview",
            value=inventory_preview,
            inline=False
        )
    
    await interaction.response.send_message(embed=embed)

@bot.event
async def on_command_error(ctx, error):
    """Handle command errors"""
    print(f"Command error: {error}")
    if isinstance(error, commands.CommandNotFound):
        return
    await ctx.send(f"❌ An error occurred: {str(error)}")

@bot.event
async def on_interaction_error(interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
    """Handle slash command errors"""
    print(f"Slash command error: {error}")
    if not interaction.response.is_done():
        await interaction.response.send_message(f"❌ An error occurred: {str(error)}", ephemeral=True)
    else:
        await interaction.followup.send(f"❌ An error occurred: {str(error)}", ephemeral=True)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if "meow" in message.content.lower():
        await message.channel.send("Meow! 🐱")
    
    await bot.process_commands(message)

bot.run(token)