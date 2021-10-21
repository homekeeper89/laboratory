import pytest
from app.config import DevelopmentConfig, ProductionConfig


@pytest.mark.parametrize(
    "cfg, expected", [(DevelopmentConfig, "dot_dev"), (ProductionConfig, "dot_prod")]
)
def test_temp(cfg, expected):
    cf = cfg()
    assert cf.DOT_ENV == expected
