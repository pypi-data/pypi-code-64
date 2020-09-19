from multiprocessing import Pool

import pytest

from sym.cli.saml_clients.aws_okta import AwsOkta
from sym.cli.tests.helpers.capture import CaptureCommand
from sym.cli.tests.saml_clients.conftest import TestContextFixture

pytestmark = [
    pytest.mark.usefixtures("click_context"),
    pytest.mark.parametrize(argnames=["constructor"], argvalues=[[AwsOkta]]),
]


def test_aws_okta(
    test_context: TestContextFixture[AwsOkta], capture_command: CaptureCommand
) -> None:
    capture_command.enqueue_outputs(
        "AWS_REGION=foobar\nAWS_FOOBAR=baz\nAWS_OKTA_SESSION_EXPIRATION=1600494616\n"
    )
    with test_context(debug=False) as aws_okta:
        with capture_command():
            aws_okta.exec("aws", "ssm", "start-session", target="i-0123456789abcdef")
    capture_command.assert_command(
        "aws-okta exec sym -- env",
        "aws-okta --debug exec sym -- false",
        "aws-okta exec sym -- true",
        "aws-okta exec sym -- aws ssm start-session --target i-0123456789abcdef",
    )


def test_aws_okta_debug(
    test_context: TestContextFixture[AwsOkta], capture_command: CaptureCommand
) -> None:
    capture_command.enqueue_outputs(
        "AWS_REGION=foobar\nAWS_FOOBAR=baz\nAWS_OKTA_SESSION_EXPIRATION=1600494616\n"
    )
    with test_context(debug=True) as aws_okta:
        with capture_command():
            aws_okta.exec("env")
    capture_command.assert_command(
        "aws-okta --debug exec sym -- env",
        "aws-okta --debug exec sym -- false",
        "aws-okta --debug exec sym -- true",
        "aws-okta --debug exec sym -- env",
    )


def test_aws_okta_multi_threads(subprocess_friendly_asserter) -> None:
    commands = (
        "aws-okta exec sym -- env",
        "aws-okta --debug exec sym -- false",
        "aws-okta exec sym -- true",
        "aws-okta exec sym -- env",
    )
    f, *args = subprocess_friendly_asserter
    with Pool(processes=4) as pool:
        pool.map(f, [(*args, commands)] * 100)
