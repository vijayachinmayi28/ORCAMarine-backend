from pathlib import Path

from app.config import settings
from app.services.mpa import check_mpa


def test_empty_mpa_dataset():
    result = check_mpa(19.076, 72.8777)
    assert result.inside_mpa is False
