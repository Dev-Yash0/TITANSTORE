# TitanXBots - Admin Settings UI (FIXED)

from bot import Bot
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import OWNER_ID
from database.database import add_admin, remove_admin, list_admins

# Temporary state memory
ADD_ADMIN_MODE = {}

# =====================================================
# /settings Command
# =====================================================

@Bot.on_message(filters.command("settings") & filters.private)
async def settings_menu(client, message):

    if message.from_user.id != OWNER_ID:
        return await message.reply_text("⛔ Access Denied.")

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ Add Admin", callback_data="add_admin")],
        [InlineKeyboardButton("➖ Remove Admin", callback_data="remove_admin")],
        [InlineKeyboardButton("📋 Admin List", callback_data="admin_list")]
    ])

    await message.reply_text(
        "<b>⚙️ Admin Settings Panel</b>\n\nSelect an option below:",
        reply_markup=keyboard
    )


# =====================================================
# ADD ADMIN MODE HANDLER
# =====================================================

@Bot.on_message(filters.private & filters.text)
async def add_admin_handler(client, message):

    if message.from_user.id != OWNER_ID:
        return

    if not ADD_ADMIN_MODE.get(message.from_user.id):
        return

    try:
        new_admin = int(message.text.strip())
    except:
        return await message.reply_text("❌ Send valid numeric User ID.")

    await add_admin(new_admin)
    ADD_ADMIN_MODE.pop(message.from_user.id, None)

    await message.reply_text(f"✅ Added <code>{new_admin}</code> as admin.")


# =====================================================
# CALLBACK HANDLER
# =====================================================

@Bot.on_callback_query()
async def admin_callbacks(client, query: CallbackQuery):

    if query.from_user.id != OWNER_ID:
        return await query.answer("⛔ Unauthorized!", show_alert=True)

    await query.answer()

    # ---------------- ADD ADMIN ----------------
    if query.data == "add_admin":

        ADD_ADMIN_MODE[query.from_user.id] = True

        await query.message.edit_text(
            "<b>➕ Add Admin</b>\n\nSend the User ID to add as admin."
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

        buttons.append(
            [InlineKeyboardButton("🔙 Back", callback_data="settings_menu")]
        )

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
            f"<b>⚠️ Confirm Removal</b>\n\nRemove admin:\n<code>{remove_id}</code> ?",
            reply_markup=keyboard
        )

    # ---------------- FINAL REMOVE ----------------
    elif query.data.startswith("remove_"):

        remove_id = int(query.data.split("_")[-1])
        await remove_admin(remove_id)

        await query.answer("✅ Admin removed!", show_alert=True)

        await query.message.edit_text(
            "<b>✅ Admin removed successfully.</b>",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Back", callback_data="settings_menu")]
            ])
        )

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

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("➕ Add Admin", callback_data="add_admin")],
            [InlineKeyboardButton("➖ Remove Admin", callback_data="remove_admin")],
            [InlineKeyboardButton("📋 Admin List", callback_data="admin_list")]
        ])

        await query.message.edit_text(
            "<b>⚙️ Admin Settings Panel</b>\n\nSelect an option below:",
            reply_markup=keyboard
        )
