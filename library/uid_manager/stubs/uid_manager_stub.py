"""Stub definitions for UID lifecycle operations as described in uid_manager.json."""

from typing import Dict


def generate_uid(identity_key: str) -> Dict[str, str]:
    """Return a placeholder response for UID generation."""
    raise NotImplementedError("Stub only; refer to uid_manager.json for implementation guidance.")


def rotate_uid(identity_key: str) -> Dict[str, str]:
    """Return a placeholder response for UID rotation."""
    raise NotImplementedError("Stub only; refer to uid_manager.json for implementation guidance.")


def revoke_uid(identity_key: str, uid: str) -> Dict[str, str]:
    """Return a placeholder response for UID revocation."""
    raise NotImplementedError("Stub only; refer to uid_manager.json for implementation guidance.")


def verify_uid(identity_key: str, uid: str) -> Dict[str, str]:
    """Return a placeholder response for UID verification."""
    raise NotImplementedError("Stub only; refer to uid_manager.json for implementation guidance.")


__all__ = [
    "generate_uid",
    "rotate_uid",
    "revoke_uid",
    "verify_uid"
]
