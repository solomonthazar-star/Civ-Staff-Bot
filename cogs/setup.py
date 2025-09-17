import discord
from discord.ext import commands
from discord import app_commands
from utils.logger import Logger

GUILD_ID = 123456789012345678  

class Setup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = Logger("config.json")

    @app_commands.command(name="setup", description="Set up staff channels (logs, tickets)")
    @app_commands.checks.has_permissions(administrator=True)
    async def setup_channels(self, interaction: discord.Interaction):
        guild = interaction.guild

        # Create staff logs channel
        log_channel = discord.utils.get(guild.text_channels, name="staff-logs")
        if not log_channel:
            log_channel = await guild.create_text_channel("staff-logs")

        # Create tickets category
        ticket_category = discord.utils.get(guild.categories, name="Tickets")
        if not ticket_category:
            ticket_category = await guild.create_category("Tickets")

        # Save setup in config
        self.logger.save_config({
            "log_channel_id": log_channel.id,
            "ticket_category_id": ticket_category.id
        })

        await interaction.response.send_message(
            f"✅ Setup complete!\n- Log channel: {log_channel.mention}\n- Ticket category: {ticket_category.name}",
            ephemeral=True
        )

async def setup(bot):
    await bot.add_cog(Setup(bot), guild=discord.Object(id=GUILD_ID))
