"""Fixtures for Roku integration tests."""
from collections.abc import Generator
import json
from unittest.mock import MagicMock, patch

import pytest
from rokuecp import Device as RokuDevice

from homeassistant.components.roku.const import DOMAIN
from homeassistant.const import CONF_HOST
from homeassistant.core import HomeAssistant

from tests.common import MockConfigEntry, load_fixture


@pytest.fixture
def mock_config_entry() -> MockConfigEntry:
    """Return the default mocked config entry."""
    return MockConfigEntry(
        title="Roku",
        domain=DOMAIN,
        data={CONF_HOST: "192.168.1.160"},
        unique_id="1GU48T017973",
    )


@pytest.fixture
def mock_roku_config_flow(
    request: pytest.FixtureRequest,
) -> Generator[None, MagicMock, None]:
    """Return a mocked Roku client."""
    with patch(
        "homeassistant.components.roku.config_flow.Roku", autospec=True
    ) as roku_mock:
        client = roku_mock.return_value
        client.update.return_value = RokuDevice(
            json.loads(load_fixture("roku/roku3.json"))
        )
        yield client


@pytest.fixture
def mock_roku(request: pytest.FixtureRequest) -> Generator[None, MagicMock, None]:
    """Return a mocked Roku client."""
    fixture: str = "roku/roku3.json"
    if hasattr(request, "param") and request.param:
        fixture = request.param

    device = RokuDevice.from_dict(json.loads(load_fixture(fixture)))
    with patch("homeassistant.components.roku.Roku", autospec=True) as roku_mock:
        client = roku_mock.return_value
        client.update.return_value = device
        yield client


@pytest.fixture
async def init_integration(
    hass: HomeAssistant, mock_config_entry: MockConfigEntry, mock_roku: MagicMock
) -> MockConfigEntry:
    """Set up the Roku integration for testing."""
    mock_config_entry.add_to_hass(hass)

    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    return mock_config_entry
