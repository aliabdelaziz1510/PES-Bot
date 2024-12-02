import discord
from discord.ext import commands
from discord import app_commands
from gdrive import *
# from _log import _logger
from logTask import logTask
import os
from dotenv import load_dotenv
import time
class send_task(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        # self.logger = _logger()
        load_dotenv(".env")

    @app_commands.command(
        name="send_task", description="All tasks should be submitted here"
    )
    async def send_task(
        self,
        interaction: discord.Interaction,
        file: discord.Attachment,
    ):
        """Command: send_task

        Parameters:
        - task_number (str): The number of the task to be submitted.
        - file (discord.Attachment): The file attachment to be submitted.

        Submits a task with the specified number and a file attachment to the designated Google Drive folder.
        """
        print("=" * 80)
        await interaction.response.defer(ephemeral=False)
        
        try:
            # user name
            user_name = interaction.user.global_name
            user_id = interaction.user
            Track_id = interaction.channel.parent_id
            print(Track_id)
            print(f"Channel_id {Track_id}")
            print("username:" + user_name)
            folder_id = {
                1298739590236082186: "1fUnf9aNaJ1StQ008abBBO-sHmaRnCzXa",  # automation-g1
                1298372720534491247: "1tOteiKJhlLUm8eLzNJIjYNf7NYbCBkjR",  # automation-g2
                1298374602552250452: "182r4vvz4honT-G-riLJvkesPVMYS0dgD",  # distribution-g1
                1298375236135419926: "1qghBLByMOpaq9WtrLm0ITsafWmbSv0GD",  # distribution-g2
                1298375343148630066: "1A1yzYPdr9Dqz9hM5IxWTpCG0MpJh29o5",  # E-Mobility
                1298374623083364433: "1Hxmri0y69kk7BujM4xxKwNWDR3XDeO8A",  # Smart Home
                1298375769239851040: "1OzKG54qR3cNae6I-MWFS2yMk4XK-ahTv",  # Mechanical
            }

            task_id = find_or_create_folder(gdrive(),folder_id[(Track_id)],interaction.channel.name)
            
            
            gfile = gdrive().CreateFile(
                {
                    "title": file.filename,
                    "parents": [{"id": task_id}],
                    # "content-length": file.size,  # Set the content length explicitly
                }
            )
            # response = requests.get(file.url)
            # file_data = BytesIO(response.content)
            respone_file = await file.read()
            # Save the file data to a temporary file
            cpath = os.getcwd()
            # temp_path = os.path.join(cpath, "temp")
            temp_file_path = os.path.join(cpath, file.filename)

            with open(temp_file_path, "wb") as temp_file:
                temp_file.write(respone_file)
            # Set the content file from the temporary file
            # print(temp_file_path)
            gfile.SetContentFile(temp_file_path)

            # Upload the file to Google Drive directly
            
            gfile.Upload()
            # Clean up the temporary file
            try:
                os.remove(temp_file_path)
            except Exception as e:
                print(f"File Removing Error: {e}")
            # Get the link to the uploaded file
            # file_url = gfile['alternateLink']

            # Send the file link as a response in Discord
            # await interaction.response.send_message(f'Uploaded file to Google Drive. You can access it [here]({file_url}).', ephemeral=True)
            # logTask(user_name, str(user_id), task_number, "---", str(file.filename))
            await interaction.followup.send(
                f"**{user_name}** successfully submitted **{interaction.channel.name}**"
            )
            # if str(user_id) not in self.Mechanical_users:
            #     self.logger.info(
            #         f"**{user_name}** successfully submitted **Task #{task_number}** Electronics"
            #     )
            # else:
            #     self.logger.info(
            #         f"**{user_name}** successfully submitted **Task #{task_number}** Mechanical"
            #     )

        except Exception as e:
            # self.logger.error(
            #     f"**{user_name}** coundn't submitted **Task #{task_number}**"
            # )
            # self.logger.error(e)
            print(e)


async def setup(client: commands.Bot) -> None:
    await client.add_cog(send_task(client))
