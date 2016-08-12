import os
from collections import OrderedDict
from datetime import datetime

import pytest
from arq import ConnectionSettings
from arq.utils import timestamp

from .fixtures import CustomSettings


def test_settings_unchanged():
    settings = ConnectionSettings()
    assert settings.R_PORT == 6379


def test_settings_changed():
    settings = ConnectionSettings(R_PORT=123)
    assert settings.R_PORT == 123
    d = OrderedDict([('R_HOST', 'localhost'), ('R_PORT', 6379), ('R_DATABASE', 0), ('R_PASSWORD', None)])
    assert isinstance(settings.dict, OrderedDict)
    assert settings.dict == d
    assert dict(settings) == dict(d)


def test_settings_invalid():
    with pytest.raises(TypeError):
        ConnectionSettings(FOOBAR=123)


def test_custom_settings():
    settings = CustomSettings()
    assert settings.dict == OrderedDict([('R_HOST', 'localhost'), ('R_PORT', 6379),
                                         ('R_DATABASE', 0), ('R_PASSWORD', None),
                                         ('X_THING', 2), ('A_THING', 1)])


def test_timestamp():
    os.environ['TZ'] = 'Asia/Singapore'
    # check we've successfully changed the timezone
    assert 7.99 < (datetime.now() - datetime.utcnow()).total_seconds() / 3600 < 8.01
    unix_stamp = int(datetime.now().strftime('%s'))
    assert abs(timestamp() - unix_stamp) < 1