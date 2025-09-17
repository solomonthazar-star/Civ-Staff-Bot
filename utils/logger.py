import json
import os
import discord

class Logger:
    def __init__(self, filename):
        self.filename = filename
        if not os.path.exists(filename):
            with open(filename, "w") as f:
                json.dump({}, f)

    def load_config(self):
        with open(self.filename, "r") as f:
            return json.load(f)

    def save_config(self, data):
        with open(self.filename, "w") as f:
            json.dump(data, f, indent=4)

    async def log_action(self, bot, guild, message):
        config = self.load_config()
        log_channel_id = config.get("log_channel_id")
        if log_channel_id:
            log_channel = guild.get_channel(log_channel_id)
            if log_channel:
                embed = discord.Embed(description=message, color=discord.Color.orange())
                await log_channel.send(embed=embed)
