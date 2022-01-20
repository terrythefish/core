"""Fixtures for Roku integration tests."""
import json
from unittest.mock import AsyncMock, MagicMock, patch

from rokuecp import x
import pytest

from homeassistant.components.roku.const import DOMAIN
from homeassistant.core import HomeAssistant

from tests.common import MockConfigEntry, load_fixture
from tests.test_util.aiohttp import AiohttpClientMocker


@pytest.fixture
def mock_config_entry() -> MockConfigEntry:
    """Return the default mocked config entry."""
    return MockConfigEntry(
        title="Roku",
        domain=DOMAIN,
        data={},
        unique_id="unique",
    )


@pytest.fixture
def mock_roku(aioclient_mock: AiohttpClientMocker):
    """Return a mocked Roku client."""
    with patch("homeassistant.components.roku.Roku") as roku_mock:
        client = roku_mock.return_value
        yield roku_mock


@pytest.fixture
async def init_integration(
    hass: HomeAssistant, mock_config_entry: MockConfigEntry, mock_roku: MagicMock
) -> MockConfigEntry:
    """Set up the Roku integration for testing."""
    mock_config_entry.add_to_hass(hass)

    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    return mock_config_entry
