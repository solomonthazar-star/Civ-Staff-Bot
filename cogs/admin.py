import discord
from discord.ext import commands
from discord import app_commands
from utils.logger import Logger

GUILD_ID = 123456789012345678  

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = Logger("config.json")

    @app_commands.command(name="ban", description="Ban a member")
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
        await member.ban(reason=reason)
        await interaction.response.send_message(f"Banned {member.mention} for: {reason}")
        await self.logger.log_action(self.bot, interaction.guild, f"🚨 **Ban:** {member} | Reason: {reason}")

    @app_commands.command(name="kick", description="Kick a member")
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
        await member.kick(reason=reason)
        await interaction.response.send_message(f"Kicked {member.mention} for: {reason}")
        await self.logger.log_action(self.bot, interaction.guild, f"⚠️ **Kick:** {member} | Reason: {reason}")

    @app_commands.command(name="clear", description="Clear messages")
    async def clear(self, interaction: discord.Interaction, amount: int):
        await interaction.channel.purge(limit=amount + 1)
        await interaction.response.send_message(f"Cleared {amount} messages.", ephemeral=True)
        await self.logger.log_action(self.bot, interaction.guild, f"🧹 **Cleared:** {amount} messages in {interaction.channel.mention}")

async def setup(bot):
    await bot.add_cog(Admin(bot), guild=discord.Object(id=GUILD_ID))
