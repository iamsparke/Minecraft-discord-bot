import discord
from mcstatus import MinecraftServer  # Using the working version after downgrading
import os

# Initialize the Discord client
intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!d'):
        command = message.content.split()
        if len(command) < 2:
            await message.channel.send("Please provide a valid command. Example: `!d info <address>:<port>`")
            return

        subcommand = command[1]
        server_address = command[2] if len(command) > 2 else None

        if server_address and ':' in server_address:
            address, port = server_address.split(':')
            port = int(port)
        else:
            address = server_address
            port = 25565

        try:
            server = MinecraftServer.lookup(f"{address}:{port}")

            if subcommand == "info":
                status = server.status()
                response = (
                    f"**Server Address:** {address}:{port}\n"
                    f"**Status:** Online\n"
                    f"**Version:** {status.version.name}\n"
                    f"**Players:** {status.players.online}/{status.players.max}\n"
                    f"**Description:** {status.description}"
                )
            elif subcommand == "ping":
                latency = server.ping()
                response = f"**Server Address:** {address}:{port}\n**Latency:** {latency:.2f} ms"
            elif subcommand == "players":
                status = server.status()
                if status.players.sample:
                    player_names = ', '.join([player.name for player in status.players.sample])
                    response = (
                        f"**Server Address:** {address}:{port}\n"
                        f"**Players Online:** {status.players.online}/{status.players.max}\n"
                        f"**Player List:** {player_names}"
                    )
                else:
                    response = f"**Server Address:** {address}:{port}\nNo players are currently online."
            elif subcommand == "coords":
                query = server.query()
                if query.players.names:
                    coords_list = []
                    for player in query.players.names:
                        # Assuming you have a method to get player coordinates
                        # This will depend on how the server exposes player data.
                        # Example: if the server exposes it through query or rcon:
                        # This part of the code is pseudo and might need modification.
                        coords = query.players[player]['coords']  # Replace with actual API call if available
                        coords_list.append(f"{player}: {coords}")
                    
                    if coords_list:
                        response = (
                            f"**Server Address:** {address}:{port}\n"
                            f"**Player Coordinates:**\n" + "\n".join(coords_list)
                        )
                    else:
                        response = f"No coordinates data available for players on {address}:{port}."
                else:
                    response = f"No players are currently online on {address}:{port}."

            else:
                response = "Unknown subcommand. Use `info`, `ping`, `players`, or `coords`."

        except Exception as e:
            response = f"Failed to retrieve server details: {e}"

        await message.channel.send(response)

TOKEN = os.getenv('DISCORD_TOKEN')
client.run(TOKEN)
# if you are using Replit then add your bot token in secrets.
