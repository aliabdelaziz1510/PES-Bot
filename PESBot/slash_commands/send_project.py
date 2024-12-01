import discord
from discord.ext import commands
from discord import app_commands
from gdrive import gdrive
from _log import _logger
from logTask import logTask
import requests
from io import BytesIO
import os
from dotenv import load_dotenv


class send_project(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.logger = _logger()
        load_dotenv(".env")

    @app_commands.command(
        name="send_project", description="All projects should be submitted here"
    )
    async def send_project(
        self, interaction: discord.Interaction, project_number: str, file: discord.Attachment
    ):
        """Command: send_project

        Parameters:
        - project_number (str): The number of the project to be submitted.
        - file (discord.Attachment): The file attachment to be submitted.

        Submits a project with the specified number and a file attachment to the designated Google Drive folder.
        """
        await interaction.response.defer(ephemeral=False)
        print("=" * 80)
        try:
            # user name
            user_name = interaction.user.global_name
            user_id = interaction.user
            print("username:" + user_name)
            # await interaction.response.send_message(f'processing...', ephemeral=True)

            # Create a GoogleDriveFile instance
            folder_id = str(os.getenv("project_folders_id"))
            gfile = gdrive().CreateFile(
                {"title": file.filename, "parents": [{"id": str(folder_id)}]}
            )
            response = requests.get(file.url)
            file_data = BytesIO(response.content)
            # Save the file data to a temporary file
            cpath = os.getcwd()
            # temp_path = os.path.join(cpath, "temp")
            temp_file_path = os.path.join(cpath, file.filename)
            with open(temp_file_path, "wb") as temp_file:
                temp_file.write(file_data.getvalue())
            # Set the content file from the temporary file
            print(temp_file_path)
            gfile.SetContentFile(temp_file_path)

            # Upload the file to Google Drive directly

            gfile.Upload()
            # Clean up the temporary file
            try:
                os.remove(temp_file_path)
            except Exception as e:
                print(f"Error: {e}")

            # Get the link to the uploaded file
            # file_url = gfile['alternateLink']
            # user name
            user_name = interaction.user.global_name
            # print('username:' + user_name)
            # Send the file link as a response in Discord
            # await interaction.response.send_message(f'Uploaded file to Google Drive. You can access it [here]({file_url}).', ephemeral=True)
            # logTask(user_name, str(user_id), '---', project_number, file.filename)
            await interaction.followup.send(
                f"**{user_name}** successfully submitted **project #{project_number}**"
            )
            self.logger.info(
                f"**{user_name}** successfully submitted **project #{project_number}**"
            )

        except Exception as e:
            self.logger.error(
                f"**{user_name}** coundn't submitted **Project #{project_number}**"
            )
            self.logger.error(e)
            print(e)


async def setup(client: commands.Bot) -> None:
    await client.add_cog(send_project(client))
