import discord
from discord.ext import commands
from discord.ui import Button, View
from discord import app_commands
import asyncio
import os


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

ADMIN_CHANNEL_ID = 1402438965977419880  # Reemplaza con el ID de tu canal privado para admins

class TicketButton(Button):
    def __init__(self):
        super().__init__(label="📩 Crear Ticket", style=discord.ButtonStyle.green)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            "✍️ Por favor, escribe tu mensaje de ticket aquí abajo (tienes 60 segundos)...",
            ephemeral=True
        )

        def check(m):
            return m.author == interaction.user and m.channel == interaction.channel

        try:
            msg = await bot.wait_for("message", timeout=60.0, check=check)
            await msg.delete()  # Borra el mensaje del usuario del canal público

            admin_channel = bot.get_channel(ADMIN_CHANNEL_ID)
            if admin_channel:
                embed = discord.Embed(title="🎫 Nuevo Ticket", color=0x00ff00)
                embed.add_field(name="Usuario", value=f"{interaction.user.mention} ({interaction.user.id})", inline=False)
                embed.add_field(name="Mensaje", value=msg.content, inline=False)
                await admin_channel.send(embed=embed)

            await interaction.followup.send(
                "✅ Tu mensaje fue enviado al **Buzón de Llantos**.",
                ephemeral=True
            )

        except asyncio.TimeoutError:
            await interaction.followup.send(
                "⏰ Tiempo agotado. No se recibió ningún mensaje.",
                ephemeral=True
            )

class TicketView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketButton())

@tree.command(name="ticket", description="Muestra el botón para enviar un mensaje al Buzón de Llantos")
async def ticket(interaction: discord.Interaction):
    embed = discord.Embed(
        title="💬 Buzón de Llantos",
        description="Haz clic en el botón para enviar un mensaje privado al equipo.",
        color=0x00ff00
    )
    await interaction.response.send_message(embed=embed, view=TicketView())

@bot.event
async def on_ready():
    await tree.sync()
    print(f"🤖 Bot conectado como {bot.user}")

TOKEN = os.getenv("DISCORD_TOKEN")  # Nombre de tu variable
bot.run(TOKEN)
