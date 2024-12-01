import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional
import requests
from io import BytesIO
import asyncio
from datetime import datetime, timedelta
from _log import _logger


class send_msg(commands.Cog):

  def __init__(self, client: commands.Bot):
    self.client = client
    self.logger = _logger()

  @app_commands.command(
      name="send_msg",
      description="Only the Chariman and Vice-Chairman who can use this function"
  )
  async def sendMsg(self,
                    interaction: discord.Interaction,
                    task_name: Optional[str] = None,
                    message_content: Optional[str] = None,
                    file: Optional[discord.Attachment] = None,
                    scheduled_time: Optional[str] = None):
    """Command: send_msg

        Parameters:
        - message_content (str): The content of the message.
        - file (Optional[discord.Attachment]): An optional file attachment.
        - scheduled_time (Optional[str]): An optional scheduled time in the format 'Year-Manth-Day HH:MM'.

        Sends a message in the specified channel. If a file is provided, it can be attached to the message.
        If a scheduled time is provided, the message will be scheduled to be sent at that time.
        """
    await interaction.response.defer(ephemeral=True)
    user_id = str(interaction.user)
    #print(interaction.user.id)
    channel = interaction.channel
    self.logger.info(f"{user_id} requested to send a message")
    self.TARGET_USER = [
        'ali.abdelazez',
        'eslam_mahmoud',
    ]
    try:
      if user_id in self.TARGET_USER:
        if channel:
          msg = await interaction.followup.send(
              f"The msg:```{message_content}```")

          # Schedule the message if a scheduled time is provided
          if scheduled_time:
            try:
              # current_date = datetime.now().date()
              scheduled_datetime = datetime.strptime(
                  f"{scheduled_time}", "%Y-%m-%d %H:%M") - timedelta(hours=2)
            except ValueError:
              await msg.edit(
                  content=
                  "Error: Invalid scheduled time format. Please use the format `Year-Month-Day HH:MM`."
              )
              self.logger.error(
                  f"Error: Invalid scheduled time format. Your scheduled_datetime is {scheduled_time}."
              )
              return
            # current time
            current_datetime = datetime.now()
            # Calculate the time difference
            time_difference = scheduled_datetime - current_datetime
            # Ensure the scheduled time is in the future
            if time_difference.total_seconds() > 0:
              # Inform the user about the scheduled time and cancellation option
              await msg.edit(
                  content=
                  f"The msg: \n```{message_content}```\nis scheduled for `{scheduled_time}`.\nRemaining time: `{time_difference}`.\nFile:```{file.filename}```\nThread:```{task_name}```"
              )
              self.logger.info(
                  f"The msg: \n\"{message_content}\"\nis scheduled for `{scheduled_time}`.\nRemaining time: `{time_difference}`.\n"
              )

              # Start listening for reactions in an asynchronous loop
              while time_difference.total_seconds() > 0:
                current_datetime = datetime.now()
                time_difference = scheduled_datetime - current_datetime

                # Sleep for a short duration to avoid blocking the event loop
                await asyncio.sleep(1)

              # Scheduled time has passed, send the message
              # await msg.edit(
              #     content="Scheduled time has passed. Sending the message now."
              # )
              self.logger.info(
                  "Scheduled time has passed. Sending the message now.")

            else:
              await msg.edit(
                  content=
                  f"Error: Scheduled time should be in the future.\nScheduled time: {scheduled_datetime},\nCurrent time: {current_datetime},\ntime difference {time_difference}"
              )
              self.logger.error(
                  f"Error: Scheduled time should be in the future.\nScheduled time: {scheduled_datetime},\nCurrent time: {current_datetime},\ntime difference {time_difference}"
              )
              return
          if task_name:
            thread = await channel.create_thread(
                name=task_name, type=discord.ChannelType.public_thread)
            channel = thread
            self.logger.info(f"User:{user_id} created a thread {task_name}")

          if file:
            # Use discord.File to send the downloaded file
            response = requests.get(file.url)
            file_data = BytesIO(response.content)
            await channel.send(message_content,
                               file=discord.File(file_data,
                                                 filename=file.filename))
            self.logger.info(
                f"{user_id} sent a msg in {channel}: \"{message_content}\" and file: {file.filename}"
            )
          else:
            await channel.send(content=message_content)
            self.logger.info(
                f"{user_id} sent a msg in {channel}: \"{message_content}\"")
          if task_name:
            try:
              discussion_channel_id = self.client.get_channel(
                  1165714663544205312)

              
              role_id = 1165717484280758414  # Replace with your role ID
              role = discord.utils.get(discussion_channel_id.guild.roles,
                                        id=role_id)

              #if role:
                 #role_mention = role.mention
                 #formatted_message = f"{role_mention}\nExciting news! A new challenge awaits you. Check The New Task"

                 #await discussion_channel_id.send(formatted_message)
               #else:
                 #self.logger.warning('Role not found in the server.')
              

            except Exception as e:
              self.logger.warning(e)

        else:
          self.logger.error(
              f"Trying to send msg for {user_id} in {channel}, msg content: \"{message_content}\""
          )
          await interaction.followup.send("Error: Channel not found.")

      else:
        await interaction.followup.send(
            "Error: You are not authorized to use this command.")
        self.logger.info("{user_id} is not authorized to use this command")
    except Exception as e:
      self.logger.error(f"An error occurred in send_msg: {e}")


async def setup(client: commands.Bot) -> None:
  await client.add_cog(send_msg(client))
