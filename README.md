# minecraft-rcon-bot

## Commands

### /rcon
Execute a command on the Minecraft server console.

**Usage:**
`/rcon [command]`

**Examples:**
- `/rcon time set day`
- `/rcon ban @telegram_username` (uses the linked nickname if available).
- Reply to a message: `/rcon ban $r` (bans the replied user's linked nickname).

---

### /nickname
Link a Minecraft nickname to a Telegram user.

**Usage:**
Reply to a user: `/nickname [minecraft_nickname]`

**Example:**
Reply to @user's message: `/nickname Steve` (links `Steve` to @user).

---

### /whitelist
Manage the Minecraft server whitelist.
If a nickname is provided, it willl be linked to the user.

**Usage:**
Reply to a user's message: `/whitelist [add/del] [optional:nickname]`

- **`add`**: Adds the replied user to the whitelist.
- **`del`**: Removes the replied user from the whitelist.

**Examples:**
- Reply to @user: `/whitelist add` (whitelists @user's linked nickname).
- Reply to @user: `/whitelist add Steve` (whitelists `Steve` and links it to @user).
- Reply to @user: `/whitelist del` (removes @user from the whitelist).
