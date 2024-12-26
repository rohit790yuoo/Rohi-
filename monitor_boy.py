try:
        user_id = int(context.args[0])
        if user_id in approved_users:
            del approved_users[user_id]
            await update.message.reply_text(f"✅ User {user_id} has been unapproved.")
        else:
            await update.message.reply_text(f"⚠️ User {user_id} is not approved.")
    except ValueError:
        await update.message.reply_text("❗ Invalid user_id format.")


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text("❗ Usage: /status <username>")
        return

    username = context.args[0]
    if username in monitored_accounts:
        await update.message.reply_text(f"📊 @{username} is being monitored for {monitored_accounts[username]}.")
    else:
        await update.message.reply_text(f"⚠️ @{username} is not being monitored.")


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text("❗ Usage: /stop <username>")
        return

    username = context.args[0]
    if username in monitored_accounts:
        del monitored_accounts[username]
        await update.message.reply_text(f"✅ Stopped monitoring @{username}.")
    else:
        await update.message.reply_text(f"⚠️ @{username} is not being monitored.")


async def monitorlist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_approved(update.message.from_user.id):
        await update.message.reply_text("❌ You are not authorized to use this command.")
        return

    if monitored_accounts:
        accounts = "\n".join([f"@{username}: {status}" for username, status in monitored_accounts.items()])
        await update.message.reply_text(f"📋 Monitored Accounts:\n{accounts}")
    else:
        await update.message.reply_text("📋 No accounts are currently being monitored.")


def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("ban", ban))
    application.add_handler(CommandHandler("unban", unban))
    application.add_handler(CommandHandler("approve", approve))
    application.add_handler(CommandHandler("unapprove", unapprove))
    application.add_handler(CommandHandler("monitorlist", monitorlist))
    application.add_handler(CommandHandler("status", status))  # Add status handler
    application.add_handler(CommandHandler("stop", stop))      # Add stop handler

    application.run_polling()


if name == "main":
    main()