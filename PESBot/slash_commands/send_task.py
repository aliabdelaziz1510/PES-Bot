import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv
from PESBot.gdrive import find_or_create_folder, gdrive
from googleapiclient.http import MediaFileUpload


class SendTask(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        load_dotenv(".env")

    @app_commands.command(
        name="send_task", description="Submit your tasks here."
    )
    async def send_task(
        self,
        interaction: discord.Interaction,
        file: discord.Attachment,
    ):
        """
        Command: send_task

        Submits a file to the Google Drive folder mapped to the user's channel.
        """
        await interaction.response.defer(ephemeral=False)

        # Define the mapping of channel IDs to folder IDs
        folder_id_mapping = {
            1298739590236082186: "1fUnf9aNaJ1StQ008abBBO-sHmaRnCzXa",  # automation-g1
            1298372720534491247: "1tOteiKJhlLUm8eLzNJIjYNf7NYbCBkjR",  # automation-g2
            1298374602552250452: "182r4vvz4honT-G-riLJvkesPVMYS0dgD",  # distribution-g1
            1298375236135419926: "1qghBLByMOpaq9WtrLm0ITsafWmbSv0GD",  # distribution-g2
            1298375343148630066: "1A1yzYPdr9Dqz9hM5IxWTpCG0MpJh29o5",  # E-Mobility
            1298374623083364433: "1Hxmri0y69kk7BujM4xxKwNWDR3XDeO8A",  # Smart Home
            1298375769239851040: "1OzKG54qR3cNae6I-MWFS2yMk4XK-ahTv",  # Mechanical
        }

        try:
            # Retrieve user and channel details
            user_name = interaction.user.global_name or interaction.user.name
            track_id = interaction.channel.parent_id

            if track_id not in folder_id_mapping:
                raise ValueError("Channel not mapped to any folder.")

            parent_folder_id = folder_id_mapping[track_id]

            # Initialize Google Drive service and get task folder
            service = gdrive()
            task_folder_id = find_or_create_folder(service, parent_folder_id, interaction.channel.name)

            if not task_folder_id:
                raise ValueError(f"Unable to create/find folder for channel: {interaction.channel.name}")

            # Read file data
            file_data = await file.read()
            temp_file_path = os.path.join(os.getcwd(), file.filename)

            # Save to a temporary file
            with open(temp_file_path, "wb") as temp_file:
                temp_file.write(file_data)

            # Upload file to Google Drive
            file_metadata = {"name": file.filename, "parents": [task_folder_id]}
            media = MediaFileUpload(temp_file_path)
            uploaded_file = service.files().create(
                body=file_metadata,
                media_body=media,
                fields="id"
            ).execute()

            # Cleanup temporary file
            os.remove(temp_file_path)

            # Notify the user
            await interaction.followup.send(
                f"**{user_name}**, your file has been successfully submitted to the task folder."
            )
            print(f"File uploaded successfully with ID: {uploaded_file['id']}")

        except Exception as e:
            # Handle errors gracefully
            error_message = f"An error occurred while processing your request: {e}"
            print(error_message)
            await interaction.followup.send(error_message)


async def setup(client: commands.Bot) -> None:
    await client.add_cog(SendTask(client))
