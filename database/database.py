# TitanXBots - Database Manager

import pymongo
from config import DB_URI, DB_NAME

# -------------------------------
# MongoDB Connection
# -------------------------------

dbclient = pymongo.MongoClient(DB_URI)
database = dbclient[DB_NAME]

user_data = database["users"]
banned_users = database["banned_users"]
admin_data = database["admins"]


# =====================================================
# USER MANAGEMENT
# =====================================================

async def present_user(user_id: int) -> bool:
    """Check if user exists in database."""
    return user_data.find_one({"_id": user_id}) is not None


async def add_user(user_id: int):
    """Add new user (if not exists)."""
    user_data.update_one(
        {"_id": user_id},
        {"$setOnInsert": {"_id": user_id}},
        upsert=True
    )


async def full_userbase() -> list:
    """Get all user IDs."""
    return [doc["_id"] for doc in user_data.find({}, {"_id": 1})]


async def del_user(user_id: int):
    """Delete user from database."""
    user_data.delete_one({"_id": user_id})


# =====================================================
# BAN / UNBAN MANAGEMENT
# =====================================================

async def is_banned(user_id: int) -> bool:
    """Check if user is banned."""
    return banned_users.find_one({"_id": user_id}) is not None


async def get_ban_reason(user_id: int) -> str:
    """Get ban reason of user."""
    data = banned_users.find_one({"_id": user_id})
    return data["reason"] if data and "reason" in data else "No reason provided"


async def ban_user(user_id: int, reason: str):
    """Ban a user with reason."""
    banned_users.update_one(
        {"_id": user_id},
        {"$set": {"reason": reason}},
        upsert=True
    )


async def unban_user(user_id: int):
    """Unban user."""
    banned_users.delete_one({"_id": user_id})

# ==============================
# ADMIN MANAGEMENT
# ==============================

async def add_admin(user_id: int):
    admin_data.update_one(
        {"_id": user_id},
        {"$setOnInsert": {"_id": user_id}},
        upsert=True
    )

async def remove_admin(user_id: int):
    admin_data.delete_one({"_id": user_id})

async def list_admins() -> list:
    return [doc["_id"] for doc in admin_data.find({}, {"_id": 1}).sort("_id", 1)]

async def is_admin(user_id: int) -> bool:
    return admin_data.find_one({"_id": user_id}) is not None
