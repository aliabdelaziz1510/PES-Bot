import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional
import requests
from io import BytesIO
import asyncio
from datetime import datetime, timedelta
from _log import _logger



class SendMessage(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.logger = _logger()
        self.TARGET_USERS = ['ali.abdelazez', 'eslam_mahmoud','amr_yasser']

    @app_commands.command(
        name="send_msg",
        description="Allows Chairman and Vice-Chairman to send messages."
    )
    async def send_msg(self,
                       interaction: discord.Interaction,
                       task_name: Optional[str] = None,
                       message_content: Optional[str] = None,
                       file: Optional[discord.Attachment] = None,
                       scheduled_time: Optional[str] = None):
        """Send a message, optionally with a file and/or schedule.

        Args:
            task_name (str, optional): Name for the thread (if any).
            message_content (str, optional): Content of the message.
            file (discord.Attachment, optional): File attachment.
            scheduled_time (str, optional): Schedule time (format: 'YYYY-MM-DD HH:MM').
        """
        await interaction.response.defer(ephemeral=True)
        user_id = str(interaction.user)
        channel = interaction.channel

        self.logger.info(f"{user_id} initiated a send_msg request.")

        if user_id not in self.TARGET_USERS:
            await interaction.followup.send("Error: Unauthorized user.")
            self.logger.warning(f"Unauthorized access by {user_id}.")
            return

        if not channel:
            await interaction.followup.send("Error: Channel not found.")
            self.logger.error(f"Channel not found for {user_id}.")
            return

        try:
            if scheduled_time:
                try:
                    scheduled_datetime = datetime.strptime(
                        scheduled_time, "%Y-%m-%d %H:%M"
                    ) - timedelta(hours=2)
                except ValueError:
                    await interaction.followup.send(
                        "Error: Invalid time format. Use `YYYY-MM-DD HH:MM`."
                    )
                    self.logger.error(f"Invalid time format: {scheduled_time}")
                    return

                current_datetime = datetime.now()
                time_difference = (scheduled_datetime - current_datetime).total_seconds()

                if time_difference <= 0:
                    await interaction.followup.send("Error: Scheduled time must be in the future.")
                    self.logger.error(f"Scheduled time in the past: {scheduled_time}")
                    return

                await interaction.followup.send(
                    f"Message scheduled for `{scheduled_time}`. Remaining time: {timedelta(seconds=time_difference)}"
                )
                self.logger.info(f"Message scheduled for {scheduled_time} by {user_id}.")

                await asyncio.sleep(time_difference)

            # Send the message
            if task_name:
                thread = await channel.create_thread(
                    name=task_name, type=discord.ChannelType.public_thread
                )
                channel = thread
                self.logger.info(f"Thread '{task_name}' created by {user_id}.")

            if file:
                response = requests.get(file.url)
                file_data = BytesIO(response.content)
                await channel.send(
                    content=message_content,
                    file=discord.File(file_data, filename=file.filename)
                )
                self.logger.info(f"Message with file sent by {user_id}: {file.filename}")
            else:
                await channel.send(content=message_content)
                self.logger.info(f"Message sent by {user_id}: {message_content}")

        except Exception as e:
            await interaction.followup.send("An error occurred while sending the message.")
            self.logger.error(f"Error in send_msg: {e}")


async def setup(client: commands.Bot):
    await client.add_cog(SendMessage(client))
