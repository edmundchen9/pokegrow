# pokegrow
Discord bot where you can feed your pokemon berries and other consumables to make them grow

## Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/edmundchen9/pokegrow.git
   cd pokegrow
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   # or
   source .venv/bin/activate  # On Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   - Copy `env.template` to `.env`
   - Fill in your Discord bot token in the `.env` file
   - Get your token from the [Discord Developer Portal](https://discord.com/developers/applications)

5. **Run the bot**
   ```bash
   python main.py
   ```

## Environment Variables

- `DISCORD_TOKEN`: Your Discord bot token (required)

## Security Note

Never commit your `.env` file! It contains sensitive information. The `.gitignore` file is configured to exclude it from version control.