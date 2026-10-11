import os
from unittest.mock import patch

import pytest

import app


def test_validate_stepora_response_rejects_misleading_ascp_mls_score_statement():
    result = app.validate_stepora_response(
        "The ASCP MLS exam with a converted passing score of at least 75.",
        "My highest education is high school.",
    )

    assert result[0] is False
    assert "converted passing score" in result[1].lower()


def test_validate_stepora_response_accepts_valid_statement():
    result = app.validate_stepora_response(
        "Current ASCP MLS certification satisfies the examination requirement.",
        "I have a chemistry degree.",
    )

    assert result == (True, "")


def test_get_openai_client_requires_env_var():
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(RuntimeError, match="NEBIUS_API_KEY"):
            app.get_openai_client()
