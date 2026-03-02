"""Utility module for generating MD5-based transaction codes."""
import datetime
import hashlib


class Md5:
    """Generate unique MD5 hashes using input + current timestamp."""

    @staticmethod
    def md5(s: str) -> str:
        """
        Generate an MD5 hash from a string and the current timestamp.

        Args:
            s: Input string to hash.

        Returns:
            A hexadecimal MD5 digest string.
        """
        ctime = str(datetime.datetime.now())
        m = hashlib.md5(bytes(s, encoding="utf-8"))
        m.update(bytes(ctime, encoding="utf-8"))
        return m.hexdigest()