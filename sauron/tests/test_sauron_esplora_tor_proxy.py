#!/usr/bin/python

import os

os.environ["TEST_NETWORK"] = "bitcoin"
import pyln
import pytest
from pyln.testing import utils
from util import *  # noqa: F403

pyln.testing.fixtures.network_daemons["bitcoin"] = utils.BitcoinD


class LightningNode(utils.LightningNode):
    def __init__(self, *args, **kwargs):
        utils.LightningNode.__init__(self, *args, **kwargs)
        lightning_dir = args[1]

        self.daemon = LightningD(lightning_dir, None)  # noqa: F405
        options = {
            "disable-plugin": "bcli",
            "network": "bitcoin",
            "plugin": os.path.join(os.path.dirname(__file__), "../sauron.py"),
            "sauron-api-endpoint": "https://blockstream.info/api",
            "sauron-tor-proxy": "localhost:9050",
        }
        self.daemon.opts.update(options)

    # Monkey patch
    def set_feerates(self, feerates, wait_for_effect=True):
        return None


@pytest.fixture
def node_cls():
    yield LightningNode


def test_tor_proxy(ln_node):
    """
    Test for tor proxy
    """

    assert ln_node.daemon.opts["sauron-tor-proxy"] == "localhost:9050"
    assert ln_node.daemon.is_in_log("Using proxy socks5h://localhost:9050 for requests")
