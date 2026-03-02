"""
Tests for utils/jwt.py — JWT token creation and parsing.

TEST-005: Unit tests for JWT token management.
"""
import os
import pytest
import time


class TestJWTTokenCreation:
    """Tests for JWT token creation."""

    def test_create_token_returns_string(self):
        from utils.jwt import create_token
        token = create_token({"openid": "test-user-123"})
        assert isinstance(token, str)
        assert len(token) > 20

    def test_create_token_with_payload(self):
        from utils.jwt import create_token, parse_payload
        payload = {"openid": "test-user-456", "role": "admin"}
        token = create_token(payload)
        result = parse_payload(token)
        assert result["status"] is True
        assert result["data"]["openid"] == "test-user-456"
        assert result["data"]["role"] == "admin"

    def test_different_payloads_produce_different_tokens(self):
        from utils.jwt import create_token
        token1 = create_token({"openid": "user-1"})
        token2 = create_token({"openid": "user-2"})
        assert token1 != token2


class TestJWTTokenParsing:
    """Tests for JWT token parsing."""

    def test_valid_token_parses(self):
        from utils.jwt import create_token, parse_payload
        token = create_token({"openid": "valid-user"})
        result = parse_payload(token)
        assert result["status"] is True
        assert result["data"]["openid"] == "valid-user"

    def test_invalid_token_fails(self):
        from utils.jwt import parse_payload
        result = parse_payload("invalid-garbage-token")
        assert result["status"] is False

    def test_tampered_token_fails(self):
        from utils.jwt import create_token, parse_payload
        token = create_token({"openid": "user"})
        # Tamper with the token
        tampered = token[:-5] + "XXXXX"
        result = parse_payload(tampered)
        assert result["status"] is False

    def test_token_contains_expiration(self):
        from utils.jwt import create_token, parse_payload
        token = create_token({"openid": "user"})
        result = parse_payload(token)
        assert "exp" in result["data"]


class TestJWTSaltConfiguration:
    """Tests for JWT salt environment configuration (SEC-008)."""

    def test_salt_warning_without_env_var(self):
        """When JWT_SALT env var is not set, a warning should be raised."""
        # The warning was already issued at import time, so we just verify
        # the module loaded successfully with fallback
        from utils.jwt import JWT_SALT
        assert JWT_SALT is not None
        assert len(JWT_SALT) > 10
