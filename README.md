# ucord

Ucord is a discord library build using threads for maximum performance

## Bot example

```python
    import ucord

    client = ucord.Client()
    client.set_token("token")
    client.run()

    @client.on_ready
    def on_ready(client):
        print(f"Logged in as {client.user}")

    @client.slash_command(name="ping", description="Ping command")
    def ping(ctx):
        embed = ucord.Embed(title="Pong!", description="Pong!")
        ctx.reply("Bot is online", embed=embed)
```