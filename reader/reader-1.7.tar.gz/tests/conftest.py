import py.path
import pytest
from utils import reload_module

from reader import make_reader
from reader._storage import Storage


def pytest_addoption(parser):
    parser.addoption(
        "--runslow", action="store_true", default=False, help="run slow tests"
    )


def pytest_collection_modifyitems(config, items):  # pragma: no cover
    if config.getoption("--runslow"):
        # --runslow given in cli: do not skip slow tests
        return
    skip_slow = pytest.mark.skip(reason="need --runslow option to run")
    for item in items:
        if "slow" in item.keywords:
            item.add_marker(skip_slow)


@pytest.fixture
def reader():
    return make_reader(':memory:')


@pytest.fixture
def storage():
    return Storage(':memory:')


def call_update_feeds(reader, _):
    reader.update_feeds()


def call_update_feeds_workers(reader, _):
    reader.update_feeds(workers=2)


def call_update_feed(reader, url):
    reader.update_feed(url)


@pytest.fixture(
    params=[
        call_update_feeds,
        pytest.param(call_update_feeds_workers, marks=pytest.mark.slow),
        call_update_feed,
    ]
)
def call_update_method(request):
    return request.param


def feed_arg_as_str(feed):
    return feed.url


def feed_arg_as_feed(feed):
    return feed


@pytest.fixture(params=[feed_arg_as_str, feed_arg_as_feed])
def feed_arg(request):
    return request.param


def entry_arg_as_tuple(entry):
    return entry.feed.url, entry.id


def entry_arg_as_entry(entry):
    return entry


@pytest.fixture(params=[entry_arg_as_tuple, entry_arg_as_entry])
def entry_arg(request):
    return request.param


@pytest.fixture
def db_path(tmpdir):
    return str(tmpdir.join('db.sqlite'))


@pytest.fixture
def data_dir():
    return py.path.local(__file__).dirpath().join('data')
