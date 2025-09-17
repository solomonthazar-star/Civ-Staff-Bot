import discord
from discord.ext import commands
from discord import app_commands
from utils.storage import TicketStorage
from utils.logger import Logger

GUILD_ID = 123456789012345678  

class TicketView(discord.ui.View):
    def __init__(self, bot, storage, logger):
        super().__init__(timeout=None)
        self.bot = bot
        self.storage = storage
        self.logger = logger

    @discord.ui.button(label="Open Ticket", style=discord.ButtonStyle.primary)
    async def open_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        config = self.logger.load_config()
        category_id = config.get("ticket_category_id")
        category = guild.get_channel(category_id) if category_id else None

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True),
        }

        ticket_channel = await guild.create_text_channel(
            name=f"ticket-{interaction.user.name}", 
            overwrites=overwrites,
            category=category
        )
        self.storage.save_ticket(interaction.user.id, ticket_channel.id)
        await self.logger.log_action(self.bot, guild, f"🎫 **Ticket Opened:** {ticket_channel.mention} by {interaction.user.mention}")
        await interaction.response.send_message(f"Ticket created: {ticket_channel.mention}", ephemeral=True)

    @discord.ui.button(label="Close Ticket", style=discord.ButtonStyle.danger)
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.channel.name.startswith("ticket-"):
            self.storage.delete_ticket(interaction.channel.id)
            await self.logger.log_action(self.bot, interaction.guild, f"✅ **Ticket Closed:** {interaction.channel.name} by {interaction.user.mention}")
            await interaction.channel.delete()
        else:
            await interaction.response.send_message("This is not a ticket channel.", ephemeral=True)


class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.storage = TicketStorage("tickets.json")
        self.logger = Logger("config.json")

    @app_commands.command(name="ticket", description="Open or close a ticket")
    async def ticket(self, interaction: discord.Interaction):
        view = TicketView(self.bot, self.storage, self.logger)
        await interaction.response.send_message("Use the buttons below to manage tickets:", view=view, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Tickets(bot), guild=discord.Object(id=GUILD_ID))
