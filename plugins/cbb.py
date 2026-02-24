# =====================================================
# IMPORTS
# =====================================================

from bot import Bot
from config import *
from Script import *
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

# Database functions
from database.database import add_admin, remove_admin, list_admins


# =====================================================
# TEMP MEMORY (STATE SYSTEM)
# =====================================================

ADD_ADMIN_MODE = {}
REMOVE_ADMIN_MODE = {}


# =====================================================
# CALLBACK HANDLER
# =====================================================

@Bot.on_callback_query()
async def cb_handler(client: Bot, query: CallbackQuery):

    data = query.data
    await query.answer()

    # =====================================================
    # START MENU
    # =====================================================
    if data == "start":
        await query.message.edit_text(
            text=START_MSG.format(first=query.from_user.first_name),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🧠 ʜᴇʟᴘ", callback_data="help"),
                        InlineKeyboardButton("🔰 ᴀʙᴏᴜᴛ", callback_data="about")
                    ],
                    [
                        InlineKeyboardButton("⚙️ ꜱᴇᴛᴛɪɴɢꜱ", callback_data="settings")
                    ]
                ]
            )
        )

    # =====================================================
    # HELP MENU
    # =====================================================
    elif data == "help":
        await query.message.edit_text(
            text=HELP_TXT.format(first=query.from_user.first_name),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🧑‍💻 ᴄᴏɴᴛᴀᴄᴛ ᴏᴡɴᴇʀ", user_id=OWNER_ID),
                        InlineKeyboardButton("💬 ᴄᴏᴍᴍᴀɴᴅꜱ", callback_data="commands")
                    ],
                    [
                        InlineKeyboardButton("⚓ ʜᴏᴍᴇ", callback_data="start"),
                        InlineKeyboardButton("⚡ ᴄʟᴏꜱᴇ", callback_data="close")
                    ]
                ]
            )
        )

    # =====================================================
    # ABOUT MENU
    # =====================================================
    elif data == "about":
        await query.message.edit_text(
            text=ABOUT_TXT.format(first=query.from_user.first_name),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("📜 ᴅɪꜱᴄʟᴀɪᴍᴇʀ", callback_data="disclaimer")
                    ],
                    [
                        InlineKeyboardButton("⚓ ʜᴏᴍᴇ", callback_data="start"),
                        InlineKeyboardButton("⚡ ᴄʟᴏꜱᴇ", callback_data="close")
                    ]
                ]
            )
        )

    # =====================================================
    # SETTINGS PANEL
    # =====================================================
    elif data == "settings":
        await query.message.edit_text(
            text="<b>⚙️ Settings Panel</b>\n\nManage bot configuration from here.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("👑 Admin Settings", callback_data="admin_settings")
                    ],
                    [
                        InlineKeyboardButton("⚓ ʜᴏᴍᴇ", callback_data="start"),
                        InlineKeyboardButton("⚡ ᴄʟᴏꜱᴇ", callback_data="close")
                    ]
                ]
            )
        )

    # =====================================================
    # ADMIN SETTINGS PANEL
    # =====================================================
    elif data == "admin_settings":

        if query.from_user.id != OWNER_ID:
            return await query.answer("⛔ Access Denied!", show_alert=True)

        await query.message.edit_text(
            text="<b>👑 Admin Control Panel</b>\n\nSelect an option below:",
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("➕ Add Admin", callback_data="add_admin")],
                    [InlineKeyboardButton("➖ Remove Admin", callback_data="remove_admin")],
                    [InlineKeyboardButton("📋 Admin List", callback_data="admin_list")],
                    [InlineKeyboardButton("🔙 Back", callback_data="settings")]
                ]
            )
        )

    # =====================================================
    # ADD ADMIN MODE
    # =====================================================
    elif data == "add_admin":

        if query.from_user.id != OWNER_ID:
            return await query.answer("⛔ Access Denied!", show_alert=True)

        ADD_ADMIN_MODE[query.from_user.id] = True

        await query.message.edit_text(
            "<b>➕ Add Admin</b>\n\nSend the User ID to add as admin.",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("🔙 Back", callback_data="admin_settings")]]
            )
        )

    # =====================================================
    # REMOVE ADMIN MODE
    # =====================================================
    elif data == "remove_admin":

        if query.from_user.id != OWNER_ID:
            return await query.answer("⛔ Access Denied!", show_alert=True)

        REMOVE_ADMIN_MODE[query.from_user.id] = True

        await query.message.edit_text(
            "<b>➖ Remove Admin</b>\n\nSend the User ID to remove.",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("🔙 Back", callback_data="admin_settings")]]
            )
        )

    # =====================================================
    # ADMIN LIST
    # =====================================================
    elif data == "admin_list":

        if query.from_user.id != OWNER_ID:
            return await query.answer("⛔ Access Denied!", show_alert=True)

        admins = await list_admins()

        if not admins:
            text = "📭 No admins found."
        else:
            text = "<b>👑 Current Admins</b>\n\n" + "\n".join(
                [f"• <code>{x}</code>" for x in admins]
            )

        await query.message.edit_text(
            text,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("🔙 Back", callback_data="admin_settings")]]
            )
        )

    # =====================================================
    # COMMANDS
    # =====================================================
    elif data == "commands":
        await query.message.edit_text(
            text=COMMANDS_TXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("🔙 Back", callback_data="help")]]
            )
        )

    # =====================================================
    # DISCLAIMER
    # =====================================================
    elif data == "disclaimer":
        await query.message.edit_text(
            text=DISCLAIMER_TXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("🔙 Back", callback_data="about")]]
            )
        )

    # =====================================================
    # CLOSE BUTTON
    # =====================================================
    elif data == "close":
        await query.message.delete()



# =====================================================
# ADMIN ID RECEIVER
# =====================================================

@Bot.on_message(filters.private & filters.text)
async def admin_id_receiver(client, message):

    if message.from_user.id != OWNER_ID:
        return

    user_id = message.from_user.id

    # ADD ADMIN
    if ADD_ADMIN_MODE.get(user_id):

        try:
            new_admin = int(message.text.strip())
        except:
            return await message.reply_text("❌ Send valid numeric User ID.")

        await add_admin(new_admin)
        ADD_ADMIN_MODE.pop(user_id, None)

        return await message.reply_text(
            f"✅ Added <code>{new_admin}</code> as admin."
        )

    # REMOVE ADMIN
    if REMOVE_ADMIN_MODE.get(user_id):

        try:
            remove_id = int(message.text.strip())
        except:
            return await message.reply_text("❌ Send valid numeric User ID.")

        await remove_admin(remove_id)
        REMOVE_ADMIN_MODE.pop(user_id, None)

        return await message.reply_text(
            f"❌ Removed <code>{remove_id}</code> from admin."
        )
