from enum import Enum

class BasicStatus(str, Enum):
    active = "active"
    inactive = "inactive"
    banned = "banned"

class TrackingStatus(str, Enum): # 'pending', 'in_progress', 'success', 'error', 'dangerous'
    pending = "pending"
    in_progress = "in_progress"
    success = "success"
    error = "error"
    dangerous = "dangerous"

class WebSettingStatus(str, Enum):
    on = "on"
    off = "off"