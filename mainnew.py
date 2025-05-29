import discord
from discord.ext import commands
from discord import app_commands
import random

intents = discord.Intents.default()
intents.members = True  # Needed to get members

bot = commands.Bot(command_prefix='!', intents=intents)

wake_phrases = [
    "Wake up, tovarischch, {mention}!",
    "Wakey wakey {mention}!",
    "Get up, soldier {mention}!",
    "Time to rise, {mention}!",
    "Arise, oh mighty sleeper {mention}!",
    "You've been summoned, {mention}!",
    "Back from the grave, {mention}!",
    "They need you, {mention}!",
    "Up and at 'em, {mention}!",
    "Rise and grind, {mention}!",
    "Comrade {mention}, your duty calls!",
    "No more rest for you, {mention}!",
    "C'mon, {mention}, we got work to do!",
    "Let’s gooooo, {mention}!",
    "Time waits for no one, {mention}!",
    "Get off the digital couch, {mention}!",
    "Alarms are for amateurs. Wake up, {mention}!",
    "He lives! {mention} is back!",
    "Welcome to the land of the living, {mention}!",
    "The prophecy foretold your awakening, {mention}!"
]

def get_unique_members(guild: discord.Guild, number: int):
    members = [m for m in guild.members if not m.bot]
    if number > len(members):
        return None  # Too many requested
    return random.sample(members, number)

def generate_revivals(guild: discord.Guild, number: int):
    selected_members = get_unique_members(guild, number)
    if not selected_members:
        return [f"Cannot revive {number} users. Only {len([m for m in guild.members if not m.bot])} available."]

    messages = []
    for user in selected_members:
        phrase = random.choice(wake_phrases).replace("{mention}", user.mention)
        messages.append(phrase)
    return messages


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} slash commands.")
    except Exception as e:
        print(f"Error syncing commands: {e}")

# Slash command
@bot.tree.command(name="revive", description="Revive some random folks!")
@app_commands.describe(number="Number of users to revive")
async def slash_revive(interaction: discord.Interaction, number: int):
    if number <= 0:
        await interaction.response.send_message("Number must be greater than zero.", ephemeral=True)
        return
    messages = generate_revivals(interaction.guild, number)
    await interaction.response.send_message("\n".join(messages))

# Run the bot
bot.run("")
