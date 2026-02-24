# TitanXBots - Admin Settings UI
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import OWNER_ID
from database.database import add_admin, remove_admin, list_admins, is_admin


# -------------------------------
# SETTINGS MENU BUTTON
# -------------------------------

@Client.on_message(filters.command("settings") & filters.private)
async def settings_menu(client, message):
    if message.from_user.id != OWNER_ID:
        return await message.reply_text("⛔ Access Denied.")

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ Add Admin", callback_data="add_admin")],
        [InlineKeyboardButton("➖ Remove Admin", callback_data="remove_admin")],
        [InlineKeyboardButton("📋 Admin List", callback_data="admin_list")],
        [InlineKeyboardButton("🔙 Back", callback_data="back_main")]
    ])

    await message.reply_text(
        "<b>⚙️ Admin Settings Panel</b>\n\nSelect an option below:",
        reply_markup=keyboard
    )


# -------------------------------
# CALLBACK HANDLER
# -------------------------------

@Client.on_callback_query()
async def admin_settings_callbacks(client, query: CallbackQuery):

    user_id = query.from_user.id

    # Owner Security
    if user_id != OWNER_ID:
        return await query.answer("⛔ Unauthorized Access!", show_alert=True)

    # ---------------- ADD ADMIN ----------------
    if query.data == "add_admin":
        await query.message.edit_text(
            "<b>➕ Add Admin</b>\n\nSend the User ID to add.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Back", callback_data="settings_menu")]
            ])
        )

    # ---------------- REMOVE ADMIN ----------------
    elif query.data == "remove_admin":

        admins = await list_admins()

        if not admins:
            return await query.answer("No admins found.", show_alert=True)

        buttons = [
            [InlineKeyboardButton(f"❌ {x}", callback_data=f"confirm_remove_{x}")]
            for x in admins
        ]

        buttons.append([InlineKeyboardButton("🔙 Back", callback_data="settings_menu")])

        await query.message.edit_text(
            "<b>➖ Remove Admin</b>\n\nSelect admin to remove:",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    # ---------------- CONFIRM REMOVE ----------------
    elif query.data.startswith("confirm_remove_"):

        remove_id = int(query.data.split("_")[-1])

        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("✅ Confirm", callback_data=f"remove_{remove_id}"),
                InlineKeyboardButton("❌ Cancel", callback_data="remove_admin")
            ]
        ])

        await query.message.edit_text(
            f"<b>⚠️ Confirm Removal</b>\n\nAre you sure you want to remove:\n<code>{remove_id}</code> ?",
            reply_markup=keyboard
        )

    elif query.data.startswith("remove_"):

        remove_id = int(query.data.split("_")[-1])
        await remove_admin(remove_id)

        await query.answer("✅ Admin removed successfully!", show_alert=True)
        await settings_menu(client, query.message)

    # ---------------- ADMIN LIST ----------------
    elif query.data == "admin_list":

        admins = await list_admins()

        if not admins:
            text = "📭 No admins found."
        else:
            text = "<b>👑 Current Admins</b>\n\n" + "\n".join(
                [f"• <code>{x}</code>" for x in admins]
            )

        await query.message.edit_text(
            text,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Back", callback_data="settings_menu")]
            ])
        )

    # ---------------- BACK BUTTON ----------------
    elif query.data == "settings_menu":
        await settings_menu(client, query.message)

    elif query.data == "back_main":
        await query.message.edit_text(
            "<b>🏠 Main Menu</b>\n\nWelcome back.",
        )
