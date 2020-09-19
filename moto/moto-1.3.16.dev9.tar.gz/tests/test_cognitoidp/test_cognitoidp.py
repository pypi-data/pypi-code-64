from __future__ import unicode_literals

import json
import os
import random
import re
import hmac
import hashlib
import base64

import requests
import uuid

import boto3

# noinspection PyUnresolvedReferences
import sure  # noqa
from botocore.exceptions import ClientError
from jose import jws, jwk, jwt
from nose.tools import assert_raises

from moto import mock_cognitoidp, settings
from moto.cognitoidp.utils import create_id
from moto.core import ACCOUNT_ID


@mock_cognitoidp
def test_create_user_pool():
    conn = boto3.client("cognito-idp", "us-west-2")

    name = str(uuid.uuid4())
    value = str(uuid.uuid4())
    result = conn.create_user_pool(PoolName=name, LambdaConfig={"PreSignUp": value})

    result["UserPool"]["Id"].should_not.be.none
    result["UserPool"]["Id"].should.match(r"[\w-]+_[0-9a-zA-Z]+")
    result["UserPool"]["Arn"].should.equal(
        "arn:aws:cognito-idp:us-west-2:{}:userpool/{}".format(
            ACCOUNT_ID, result["UserPool"]["Id"]
        )
    )
    result["UserPool"]["Name"].should.equal(name)
    result["UserPool"]["LambdaConfig"]["PreSignUp"].should.equal(value)


@mock_cognitoidp
def test_list_user_pools():
    conn = boto3.client("cognito-idp", "us-west-2")

    name = str(uuid.uuid4())
    conn.create_user_pool(PoolName=name)
    result = conn.list_user_pools(MaxResults=10)
    result["UserPools"].should.have.length_of(1)
    result["UserPools"][0]["Name"].should.equal(name)


@mock_cognitoidp
def test_list_user_pools_returns_max_items():
    conn = boto3.client("cognito-idp", "us-west-2")

    # Given 10 user pools
    pool_count = 10
    for i in range(pool_count):
        conn.create_user_pool(PoolName=str(uuid.uuid4()))

    max_results = 5
    result = conn.list_user_pools(MaxResults=max_results)
    result["UserPools"].should.have.length_of(max_results)
    result.should.have.key("NextToken")


@mock_cognitoidp
def test_list_user_pools_returns_next_tokens():
    conn = boto3.client("cognito-idp", "us-west-2")

    # Given 10 user pool clients
    pool_count = 10
    for i in range(pool_count):
        conn.create_user_pool(PoolName=str(uuid.uuid4()))

    max_results = 5
    result = conn.list_user_pools(MaxResults=max_results)
    result["UserPools"].should.have.length_of(max_results)
    result.should.have.key("NextToken")

    next_token = result["NextToken"]
    result_2 = conn.list_user_pools(MaxResults=max_results, NextToken=next_token)
    result_2["UserPools"].should.have.length_of(max_results)
    result_2.shouldnt.have.key("NextToken")


@mock_cognitoidp
def test_list_user_pools_when_max_items_more_than_total_items():
    conn = boto3.client("cognito-idp", "us-west-2")

    # Given 10 user pool clients
    pool_count = 10
    for i in range(pool_count):
        conn.create_user_pool(PoolName=str(uuid.uuid4()))

    max_results = pool_count + 5
    result = conn.list_user_pools(MaxResults=max_results)
    result["UserPools"].should.have.length_of(pool_count)
    result.shouldnt.have.key("NextToken")


@mock_cognitoidp
def test_describe_user_pool():
    conn = boto3.client("cognito-idp", "us-west-2")

    name = str(uuid.uuid4())
    value = str(uuid.uuid4())
    user_pool_details = conn.create_user_pool(
        PoolName=name, LambdaConfig={"PreSignUp": value}
    )

    result = conn.describe_user_pool(UserPoolId=user_pool_details["UserPool"]["Id"])
    result["UserPool"]["Name"].should.equal(name)
    result["UserPool"]["LambdaConfig"]["PreSignUp"].should.equal(value)


@mock_cognitoidp
def test_delete_user_pool():
    conn = boto3.client("cognito-idp", "us-west-2")

    user_pool_id = conn.create_user_pool(PoolName=str(uuid.uuid4()))["UserPool"]["Id"]
    conn.list_user_pools(MaxResults=10)["UserPools"].should.have.length_of(1)
    conn.delete_user_pool(UserPoolId=user_pool_id)
    conn.list_user_pools(MaxResults=10)["UserPools"].should.have.length_of(0)


@mock_cognitoidp
def test_create_user_pool_domain():
    conn = boto3.client("cognito-idp", "us-west-2")

    domain = str(uuid.uuid4())
    user_pool_id = conn.create_user_pool(PoolName=str(uuid.uuid4()))["UserPool"]["Id"]
    result = conn.create_user_pool_domain(UserPoolId=user_pool_id, Domain=domain)
    result["ResponseMetadata"]["HTTPStatusCode"].should.equal(200)


@mock_cognitoidp
def test_create_user_pool_domain_custom_domain_config():
    conn = boto3.client("cognito-idp", "us-west-2")

    domain = str(uuid.uuid4())
    custom_domain_config = {
        "CertificateArn": "arn:aws:acm:us-east-1:{}:certificate/123456789012".format(
            ACCOUNT_ID
        )
    }
    user_pool_id = conn.create_user_pool(PoolName=str(uuid.uuid4()))["UserPool"]["Id"]
    result = conn.create_user_pool_domain(
        UserPoolId=user_pool_id, Domain=domain, CustomDomainConfig=custom_domain_config
    )
    result["ResponseMetadata"]["HTTPStatusCode"].should.equal(200)
    result["CloudFrontDomain"].should.equal("e2c343b3293ee505.cloudfront.net")


@mock_cognitoidp
def test_describe_user_pool_domain():
    conn = boto3.client("cognito-idp", "us-west-2")

    domain = str(uuid.uuid4())
    user_pool_id = conn.create_user_pool(PoolName=str(uuid.uuid4()))["UserPool"]["Id"]
    conn.create_user_pool_domain(UserPoolId=user_pool_id, Domain=domain)
    result = conn.describe_user_pool_domain(Domain=domain)
    result["DomainDescription"]["Domain"].should.equal(domain)
    result["DomainDescription"]["UserPoolId"].should.equal(user_pool_id)
    result["DomainDescription"]["AWSAccountId"].should_not.be.none


@mock_cognitoidp
def test_delete_user_pool_domain():
    conn = boto3.client("cognito-idp", "us-west-2")

    domain = str(uuid.uuid4())
    user_pool_id = conn.create_user_pool(PoolName=str(uuid.uuid4()))["UserPool"]["Id"]
    conn.create_user_pool_domain(UserPoolId=user_pool_id, Domain=domain)
    result = conn.delete_user_pool_domain(UserPoolId=user_pool_id, Domain=domain)
    result["ResponseMetadata"]["HTTPStatusCode"].should.equal(200)
    result = conn.describe_user_pool_domain(Domain=domain)
    # This is a surprising behavior of the real service: describing a missing domain comes
    # back with status 200 and a DomainDescription of {}
    result["ResponseMetadata"]["HTTPStatusCode"].should.equal(200)
    result["DomainDescription"].keys().should.have.length_of(0)


@mock_cognitoidp
def test_update_user_pool_domain():
    conn = boto3.client("cognito-idp", "us-west-2")

    domain = str(uuid.uuid4())
    custom_domain_config = {
        "CertificateArn": "arn:aws:acm:us-east-1:{}:certificate/123456789012".format(
            ACCOUNT_ID
        )
    }
    user_pool_id = conn.create_user_pool(PoolName=str(uuid.uuid4()))["UserPool"]["Id"]
    conn.create_user_pool_domain(UserPoolId=user_pool_id, Domain=domain)
    result = conn.update_user_pool_domain(
        UserPoolId=user_pool_id, Domain=domain, CustomDomainConfig=custom_domain_config
    )
    result["ResponseMetadata"]["HTTPStatusCode"].should.equal(200)
    result["CloudFrontDomain"].should.equal("e2c343b3293ee505.cloudfront.net")


@mock_cognitoidp
def test_create_user_pool_client():
    conn = boto3.client("cognito-idp", "us-west-2")

    client_name = str(uuid.uuid4())
    value = str(uuid.uuid4())
    user_pool_id = conn.create_user_pool(PoolName=str(uuid.uuid4()))["UserPool"]["Id"]
    result = conn.create_user_pool_client(
        UserPoolId=user_pool_id, ClientName=client_name, CallbackURLs=[value]
    )

    result["UserPoolClient"]["UserPoolId"].should.equal(user_pool_id)
    bool(re.match(r"^[0-9a-z]{26}$", result["UserPoolClient"]["ClientId"])).should.be.ok
    result["UserPoolClient"]["ClientName"].should.equal(client_name)
    result["UserPoolClient"].should_not.have.key("ClientSecret")
    result["UserPoolClient"]["CallbackURLs"].should.have.length_of(1)
    result["UserPoolClient"]["CallbackURLs"][0].should.equal(value)


@mock_cognitoidp
def test_create_user_pool_client_returns_secret():
    conn = boto3.client("cognito-idp", "us-west-2")

    client_name = str(uuid.uuid4())
    value = str(uuid.uuid4())
    user_pool_id = conn.create_user_pool(PoolName=str(uuid.uuid4()))["UserPool"]["Id"]
    result = conn.create_user_pool_client(
        UserPoolId=user_pool_id,
        ClientName=client_name,
        GenerateSecret=True,
        CallbackURLs=[value],
    )

    result["UserPoolClient"]["UserPoolId"].should.equal(user_pool_id)
    bool(re.match(r"^[0-9a-z]{26}$", result["UserPoolClient"]["ClientId"])).should.be.ok
    result["UserPoolClient"]["ClientName"].should.equal(client_name)
    result["UserPoolClient"]["ClientSecret"].should_not.be.none
    result["UserPoolClient"]["CallbackURLs"].should.have.length_of(1)
    result["UserPoolClient"]["CallbackURLs"][0].should.equal(value)


@mock_cognitoidp
def test_list_user_pool_clients():
    conn = boto3.client("cognito-idp", "us-west-2")

    client_name = str(uuid.uuid4())
    user_pool_id = conn.create_user_pool(PoolName=str(uuid.uuid4()))["UserPool"]["Id"]
    conn.create_user_pool_client(UserPoolId=user_pool_id, ClientName=client_name)
    result = conn.list_user_pool_clients(UserPoolId=user_pool_id, MaxResults=10)
    result["UserPoolClients"].should.have.length_of(1)
    result["UserPoolClients"][0]["ClientName"].should.equal(client_name)


@mock_cognitoidp
def test_list_user_pool_clients_returns_max_items():
    conn = boto3.client("cognito-idp", "us-west-2")
    user_pool_id = conn.create_user_pool(PoolName=str(uuid.uuid4()))["UserPool"]["Id"]

    # Given 10 user pool clients
    client_count = 10
    for i in range(client_count):
        client_name = str(uuid.uuid4())
        conn.create_user_pool_client(UserPoolId=user_pool_id, ClientName=client_name)
    max_results = 5
    result = conn.list_user_pool_clients(
        UserPoolId=user_pool_id, MaxResults=max_results
    )
    result["UserPoolClients"].should.have.length_of(max_results)
    result.should.have.key("NextToken")


@mock_cognitoidp
def test_list_user_pool_clients_returns_next_tokens():
    conn = boto3.client("cognito-idp", "us-west-2")
    user_pool_id = conn.create_user_pool(PoolName=str(uuid.uuid4()))["UserPool"]["Id"]

    # Given 10 user pool clients
    client_count = 10
    for i in range(client_count):
        client_name = str(uuid.uuid4())
        conn.create_user_pool_client(UserPoolId=user_pool_id, ClientName=client_name)
    max_results = 5
    result = conn.list_user_pool_clients(
        UserPoolId=user_pool_id, MaxResults=max_results
    )
    result["UserPoolClients"].should.have.length_of(max_results)
    result.should.have.key("NextToken")

    next_token = result["NextToken"]
    result_2 = conn.list_user_pool_clients(
        UserPoolId=user_pool_id, MaxResults=max_results, NextToken=next_token
    )
    result_2["UserPoolClients"].should.have.length_of(max_results)
    result_2.shouldnt.have.key("NextToken")


@mock_cognitoidp
def test_list_user_pool_clients_when_max_items_more_than_total_items():
    conn = boto3.client("cognito-idp", "us-west-2")
    user_pool_id = conn.create_user_pool(PoolName=str(uuid.uuid4()))["UserPool"]["Id"]

    # Given 10 user pool clients
    client_count = 10
    for i in range(client_count):
        client_name = str(uuid.uuid4())
        conn.create_user_pool_client(UserPoolId=user_pool_id, ClientName=client_name)
    max_results = client_count + 5
    result = conn.list_user_pool_clients(
        UserPoolId=user_pool_id, MaxResults=max_results
    )
    result["UserPoolClients"].should.have.length_of(client_count)
    result.shouldnt.have.key("NextToken")


@mock_cognitoidp
def test_describe_user_pool_client():
    conn = boto3.client("cognito-idp", "us-west-2")

    client_name = str(uuid.uuid4())
    value = str(uuid.uuid4())
    user_pool_id = conn.create_user_pool(PoolName=str(uuid.uuid4()))["UserPool"]["Id"]
    client_details = conn.create_user_pool_client(
        UserPoolId=user_pool_id, ClientName=client_name, CallbackURLs=[value]
    )

    result = conn.describe_user_pool_client(
        UserPoolId=user_pool_id, ClientId=client_details["UserPoolClient"]["ClientId"]
    )

    result["UserPoolClient"]["ClientName"].should.equal(client_name)
    result["UserPoolClient"]["CallbackURLs"].should.have.length_of(1)
    result["UserPoolClient"]["CallbackURLs"][0].should.equal(value)


@mock_cognitoidp
def test_update_user_pool_client():
    conn = boto3.client("cognito-idp", "us-west-2")

    old_client_name = str(uuid.uuid4())
    new_client_name = str(uuid.uuid4())
    old_value = str(uuid.uuid4())
    new_value = str(uuid.uuid4())
    user_pool_id = conn.create_user_pool(PoolName=str(uuid.uuid4()))["UserPool"]["Id"]
    client_details = conn.create_user_pool_client(
        UserPoolId=user_pool_id, ClientName=old_client_name, CallbackURLs=[old_value]
    )

    result = conn.update_user_pool_client(
        UserPoolId=user_pool_id,
        ClientId=client_details["UserPoolClient"]["ClientId"],
        ClientName=new_client_name,
        CallbackURLs=[new_value],
    )

    result["UserPoolClient"]["ClientName"].should.equal(new_client_name)
    result["UserPoolClient"].should_not.have.key("ClientSecret")
    result["UserPoolClient"]["CallbackURLs"].should.have.length_of(1)
    result["UserPoolClient"]["CallbackURLs"][0].should.equal(new_value)


@mock_cognitoidp
def test_update_user_pool_client_returns_secret():
    conn = boto3.client("cognito-idp", "us-west-2")

    old_client_name = str(uuid.uuid4())
    new_client_name = str(uuid.uuid4())
    old_value = str(uuid.uuid4())
    new_value = str(uuid.uuid4())
    user_pool_id = conn.create_user_pool(PoolName=str(uuid.uuid4()))["UserPool"]["Id"]
    client_details = conn.create_user_pool_client(
        UserPoolId=user_pool_id,
        ClientName=old_client_name,
        GenerateSecret=True,
        CallbackURLs=[old_value],
    )
    client_secret = client_details["UserPoolClient"]["ClientSecret"]

    result = conn.update_user_pool_client(
        UserPoolId=user_pool_id,
        ClientId=client_details["UserPoolClient"]["ClientId"],
        ClientName=new_client_name,
        CallbackURLs=[new_value],
    )

    result["UserPoolClient"]["ClientName"].should.equal(new_client_name)
    result["UserPoolClient"]["ClientSecret"].should.equal(client_secret)
    result["UserPoolClient"]["CallbackURLs"].should.have.length_of(1)
    result["UserPoolClient"]["CallbackURLs"][0].should.equal(new_value)


@mock_cognitoidp
def test_delete_user_pool_client():
    conn = boto3.client("cognito-idp", "us-west-2")

    user_pool_id = conn.create_user_pool(PoolName=str(uuid.uuid4()))["UserPool"]["Id"]
    client_details = conn.create_user_pool_client(
        UserPoolId=user_pool_id, ClientName=str(uuid.uuid4())
    )

    conn.delete_user_pool_client(
        UserPoolId=user_pool_id, ClientId=client_details["UserPoolClient"]["ClientId"]
    )

    caught = False
    try:
        conn.describe_user_pool_client(
            UserPoolId=user_pool_id,
            ClientId=client_details["UserPoolClient"]["ClientId"],
        )
    except conn.exceptions.ResourceNotFoundException:
        caught = True

    caught.should.be.true


@mock_cognitoidp
def test_create_identity_provider():
    conn = boto3.client("cognito-idp", "us-west-2")

    provider_name = str(uuid.uuid4())
    provider_type = "Facebook"
    value = str(uuid.uuid4())
    user_pool_id = conn.create_user_pool(PoolName=str(uuid.uuid4()))["UserPool"]["Id"]
    result = conn.create_identity_provider(
        UserPoolId=user_pool_id,
        ProviderName=provider_name,
        ProviderType=provider_type,
        ProviderDetails={"thing": value},
    )

    result["IdentityProvider"]["UserPoolId"].should.equal(user_pool_id)
    result["IdentityProvider"]["ProviderName"].should.equal(provider_name)
    result["IdentityProvider"]["ProviderType"].should.equal(provider_type)
    result["IdentityProvider"]["ProviderDetails"]["thing"].should.equal(value)


@mock_cognitoidp
def test_list_identity_providers():
    conn = boto3.client("cognito-idp", "us-west-2")

    provider_name = str(uuid.uuid4())
    provider_type = "Facebook"
    user_pool_id = conn.create_user_pool(PoolName=str(uuid.uuid4()))["UserPool"]["Id"]
    conn.create_identity_provider(
        UserPoolId=user_pool_id,
        ProviderName=provider_name,
        ProviderType=provider_type,
        ProviderDetails={},
    )

    result = conn.list_identity_providers(UserPoolId=user_pool_id, MaxResults=10)

    result["Providers"].should.have.length_of(1)
    result["Providers"][0]["ProviderName"].should.equal(provider_name)
    result["Providers"][0]["ProviderType"].should.equal(provider_type)


@mock_cognitoidp
def test_list_identity_providers_returns_max_items():
    conn = boto3.client("cognito-idp", "us-west-2")
    user_pool_id = conn.create_user_pool(PoolName=str(uuid.uuid4()))["UserPool"]["Id"]

    # Given 10 identity providers linked to a user pool
    identity_provider_count = 10
    for i in range(identity_provider_count):
        provider_name = str(uuid.uuid4())
        provider_type = "Facebook"
        conn.create_identity_provider(
            UserPoolId=user_pool_id,
            ProviderName=provider_name,
            ProviderType=provider_type,
            ProviderDetails={},
        )

    max_results = 5
    result = conn.list_identity_providers(
        UserPoolId=user_pool_id, MaxResults=max_results
    )
    result["Providers"].should.have.length_of(max_results)
    result.should.have.key("NextToken")


@mock_cognitoidp
def test_list_identity_providers_returns_next_tokens():
    conn = boto3.client("cognito-idp", "us-west-2")
    user_pool_id = conn.create_user_pool(PoolName=str(uuid.uuid4()))["UserPool"]["Id"]

    # Given 10 identity providers linked to a user pool
    identity_provider_count = 10
    for i in range(identity_provider_count):
        provider_name = str(uuid.uuid4())
        provider_type = "Facebook"
        conn.create_identity_provider(
            UserPoolId=user_pool_id,
            ProviderName=provider_name,
            ProviderType=provider_type,
            ProviderDetails={},
        )

    max_results = 5
    result = conn.list_identity_providers(
        UserPoolId=user_pool_id, MaxResults=max_results
    )
    result["Providers"].should.have.length_of(max_results)
    result.should.have.key("NextToken")

    next_token = result["NextToken"]
    result_2 = conn.list_identity_providers(
        UserPoolId=user_pool_id, MaxResults=max_results, NextToken=next_token
    )
    result_2["Providers"].should.have.length_of(max_results)
    result_2.shouldnt.have.key("NextToken")


@mock_cognitoidp
def test_list_identity_providers_when_max_items_more_than_total_items():
    conn = boto3.client("cognito-idp", "us-west-2")
    user_pool_id = conn.create_user_pool(PoolName=str(uuid.uuid4()))["UserPool"]["Id"]

    # Given 10 identity providers linked to a user pool
    identity_provider_count = 10
    for i in range(identity_provider_count):
        provider_name = str(uuid.uuid4())
        provider_type = "Facebook"
        conn.create_identity_provider(
            UserPoolId=user_pool_id,
            ProviderName=provider_name,
            ProviderType=provider_type,
            ProviderDetails={},
        )

    max_results = identity_provider_count + 5
    result = conn.list_identity_providers(
        UserPoolId=user_pool_id, MaxResults=max_results
    )
    result["Providers"].should.have.length_of(identity_provider_count)
    result.shouldnt.have.key("NextToken")


@mock_cognitoidp
def test_describe_identity_providers():
    conn = boto3.client("cognito-idp", "us-west-2")

    provider_name = str(uuid.uuid4())
    provider_type = "Facebook"
    value = str(uuid.uuid4())
    user_pool_id = conn.create_user_pool(PoolName=str(uuid.uuid4()))["UserPool"]["Id"]
    conn.create_identity_provider(
        UserPoolId=user_pool_id,
        ProviderName=provider_name,
        ProviderType=provider_type,
        ProviderDetails={"thing": value},
    )

    result = conn.describe_identity_provider(
        UserPoolId=user_pool_id, ProviderName=provider_name
    )

    result["IdentityProvider"]["UserPoolId"].should.equal(user_pool_id)
    result["IdentityProvider"]["ProviderName"].should.equal(provider_name)
    result["IdentityProvider"]["ProviderType"].should.equal(provider_type)
    result["IdentityProvider"]["ProviderDetails"]["thing"].should.equal(value)


@mock_cognitoidp
def test_update_identity_provider():
    conn = boto3.client("cognito-idp", "us-west-2")

    provider_name = str(uuid.uuid4())
    provider_type = "Facebook"
    value = str(uuid.uuid4())
    new_value = str(uuid.uuid4())
    user_pool_id = conn.create_user_pool(PoolName=str(uuid.uuid4()))["UserPool"]["Id"]
    conn.create_identity_provider(
        UserPoolId=user_pool_id,
        ProviderName=provider_name,
        ProviderType=provider_type,
        ProviderDetails={"thing": value},
    )

    result = conn.update_identity_provider(
        UserPoolId=user_pool_id,
        ProviderName=provider_name,
        ProviderDetails={"thing": new_value},
    )

    result["IdentityProvider"]["UserPoolId"].should.equal(user_pool_id)
    result["IdentityProvider"]["ProviderName"].should.equal(provider_name)
    result["IdentityProvider"]["ProviderType"].should.equal(provider_type)
    result["IdentityProvider"]["ProviderDetails"]["thing"].should.equal(new_value)


@mock_cognitoidp
def test_update_identity_provider_no_user_pool():
    conn = boto3.client("cognito-idp", "us-west-2")

    new_value = str(uuid.uuid4())

    with assert_raises(conn.exceptions.ResourceNotFoundException) as cm:
        conn.update_identity_provider(
            UserPoolId="foo", ProviderName="bar", ProviderDetails={"thing": new_value}
        )

    cm.exception.operation_name.should.equal("UpdateIdentityProvider")
    cm.exception.response["Error"]["Code"].should.equal("ResourceNotFoundException")
    cm.exception.response["ResponseMetadata"]["HTTPStatusCode"].should.equal(400)


@mock_cognitoidp
def test_update_identity_provider_no_identity_provider():
    conn = boto3.client("cognito-idp", "us-west-2")

    provider_name = str(uuid.uuid4())
    provider_type = "Facebook"
    value = str(uuid.uuid4())
    new_value = str(uuid.uuid4())
    user_pool_id = conn.create_user_pool(PoolName=str(uuid.uuid4()))["UserPool"]["Id"]

    with assert_raises(conn.exceptions.ResourceNotFoundException) as cm:
        conn.update_identity_provider(
            UserPoolId=user_pool_id,
            ProviderName="foo",
            ProviderDetails={"thing": new_value},
        )

    cm.exception.operation_name.should.equal("UpdateIdentityProvider")
    cm.exception.response["Error"]["Code"].should.equal("ResourceNotFoundException")
    cm.exception.response["ResponseMetadata"]["HTTPStatusCode"].should.equal(400)


@mock_cognitoidp
def test_delete_identity_providers():
    conn = boto3.client("cognito-idp", "us-west-2")

    provider_name = str(uuid.uuid4())
    provider_type = "Facebook"
    value = str(uuid.uuid4())
    user_pool_id = conn.create_user_pool(PoolName=str(uuid.uuid4()))["UserPool"]["Id"]
    conn.create_identity_provider(
        UserPoolId=user_pool_id,
        ProviderName=provider_name,
        ProviderType=provider_type,
        ProviderDetails={"thing": value},
    )

    conn.delete_identity_provider(UserPoolId=user_pool_id, ProviderName=provider_name)

    caught = False
    try:
        conn.describe_identity_provider(
            UserPoolId=user_pool_id, ProviderName=provider_name
        )
    except conn.exceptions.ResourceNotFoundException:
        caught = True

    caught.should.be.true


@mock_cognitoidp
def test_create_group():
    conn = boto3.client("cognito-idp", "us-west-2")

    user_pool_id = conn.create_user_pool(PoolName=str(uuid.uuid4()))["UserPool"]["Id"]
    group_name = str(uuid.uuid4())
    description = str(uuid.uuid4())
    role_arn = "arn:aws:iam:::role/my-iam-role"
    precedence = random.randint(0, 100000)

    result = conn.create_group(
        GroupName=group_name,
        UserPoolId=user_pool_id,
        Description=description,
        RoleArn=role_arn,
        Precedence=precedence,
    )

    result["Group"]["GroupName"].should.equal(group_name)
    result["Group"]["UserPoolId"].should.equal(user_pool_id)
    result["Group"]["Description"].should.equal(description)
    result["Group"]["RoleArn"].should.equal(role_arn)
    result["Group"]["Precedence"].should.equal(precedence)
    result["Group"]["LastModifiedDate"].should.be.a("datetime.datetime")
    result["Group"]["CreationDate"].should.be.a("datetime.datetime")


@mock_cognitoidp
def test_create_group_with_duplicate_name_raises_error():
    conn = boto3.client("cognito-idp", "us-west-2")

    user_pool_id = conn.create_user_pool(PoolName=str(uuid.uuid4()))["UserPool"]["Id"]
    group_name = str(uuid.uuid4())

    conn.create_group(GroupName=group_name, UserPoolId=user_pool_id)

    with assert_raises(ClientError) as cm:
        conn.create_group(GroupName=group_name, UserPoolId=user_pool_id)
    cm.exception.operation_name.should.equal("CreateGroup")
    cm.exception.response["Error"]["Code"].should.equal("GroupExistsException")
    cm.exception.response["ResponseMetadata"]["HTTPStatusCode"].should.equal(400)


@mock_cognitoidp
def test_get_group():
    conn = boto3.client("cognito-idp", "us-west-2")

    user_pool_id = conn.create_user_pool(PoolName=str(uuid.uuid4()))["UserPool"]["Id"]
    group_name = str(uuid.uuid4())
    conn.create_group(GroupName=group_name, UserPoolId=user_pool_id)

    result = conn.get_group(GroupName=group_name, UserPoolId=user_pool_id)

    result["Group"]["GroupName"].should.equal(group_name)
    result["Group"]["UserPoolId"].should.equal(user_pool_id)
    result["Group"]["LastModifiedDate"].should.be.a("datetime.datetime")
    result["Group"]["CreationDate"].should.be.a("datetime.datetime")


@mock_cognitoidp
def test_list_groups():
    conn = boto3.client("cognito-idp", "us-west-2")

    user_pool_id = conn.create_user_pool(PoolName=str(uuid.uuid4()))["UserPool"]["Id"]
    group_name = str(uuid.uuid4())
    conn.create_group(GroupName=group_name, UserPoolId=user_pool_id)

    result = conn.list_groups(UserPoolId=user_pool_id)

    result["Groups"].should.have.length_of(1)
    result["Groups"][0]["GroupName"].should.equal(group_name)


@mock_cognitoidp
def test_delete_group():
    conn = boto3.client("cognito-idp", "us-west-2")

    user_pool_id = conn.create_user_pool(PoolName=str(uuid.uuid4()))["UserPool"]["Id"]
    group_name = str(uuid.uuid4())
    conn.create_group(GroupName=group_name, UserPoolId=user_pool_id)

    result = conn.delete_group(GroupName=group_name, UserPoolId=user_pool_id)
    list(result.keys()).should.equal(["ResponseMetadata"])  # No response expected

    with assert_raises(ClientError) as cm:
        conn.get_group(GroupName=group_name, UserPoolId=user_pool_id)
    cm.exception.response["Error"]["Code"].should.equal("ResourceNotFoundException")


@mock_cognitoidp
def test_admin_add_user_to_group():
    conn = boto3.client("cognito-idp", "us-west-2")

    user_pool_id = conn.create_user_pool(PoolName=str(uuid.uuid4()))["UserPool"]["Id"]
    group_name = str(uuid.uuid4())
    conn.create_group(GroupName=group_name, UserPoolId=user_pool_id)

    username = str(uuid.uuid4())
    conn.admin_create_user(UserPoolId=user_pool_id, Username=username)

    result = conn.admin_add_user_to_group(
        UserPoolId=user_pool_id, Username=username, GroupName=group_name
    )
    list(result.keys()).should.equal(["ResponseMetadata"])  # No response expected


@mock_cognitoidp
def test_admin_add_user_to_group_again_is_noop():
    conn = boto3.client("cognito-idp", "us-west-2")

    user_pool_id = conn.create_user_pool(PoolName=str(uuid.uuid4()))["UserPool"]["Id"]
    group_name = str(uuid.uuid4())
    conn.create_group(GroupName=group_name, UserPoolId=user_pool_id)

    username = str(uuid.uuid4())
    conn.admin_create_user(UserPoolId=user_pool_id, Username=username)

    conn.admin_add_user_to_group(
        UserPoolId=user_pool_id, Username=username, GroupName=group_name
    )
    conn.admin_add_user_to_group(
        UserPoolId=user_pool_id, Username=username, GroupName=group_name
    )


@mock_cognitoidp
def test_list_users_in_group():
    conn = boto3.client("cognito-idp", "us-west-2")

    user_pool_id = conn.create_user_pool(PoolName=str(uuid.uuid4()))["UserPool"]["Id"]
    group_name = str(uuid.uuid4())
    conn.create_group(GroupName=group_name, UserPoolId=user_pool_id)

    username = str(uuid.uuid4())
    conn.admin_create_user(UserPoolId=user_pool_id, Username=username)

    conn.admin_add_user_to_group(
        UserPoolId=user_pool_id, Username=username, GroupName=group_name
    )

    result = conn.list_users_in_group(UserPoolId=user_pool_id, GroupName=group_name)

    result["Users"].should.have.length_of(1)
    result["Users"][0]["Username"].should.equal(username)


@mock_cognitoidp
def test_list_users_in_group_ignores_deleted_user():
    conn = boto3.client("cognito-idp", "us-west-2")

    user_pool_id = conn.create_user_pool(PoolName=str(uuid.uuid4()))["UserPool"]["Id"]
    group_name = str(uuid.uuid4())
    conn.create_group(GroupName=group_name, UserPoolId=user_pool_id)

    username = str(uuid.uuid4())
    conn.admin_create_user(UserPoolId=user_pool_id, Username=username)
    username2 = str(uuid.uuid4())
    conn.admin_create_user(UserPoolId=user_pool_id, Username=username2)

    conn.admin_add_user_to_group(
        UserPoolId=user_pool_id, Username=username, GroupName=group_name
    )
    conn.admin_add_user_to_group(
        UserPoolId=user_pool_id, Username=username2, GroupName=group_name
    )
    conn.admin_delete_user(UserPoolId=user_pool_id, Username=username)

    result = conn.list_users_in_group(UserPoolId=user_pool_id, GroupName=group_name)

    result["Users"].should.have.length_of(1)
    result["Users"][0]["Username"].should.equal(username2)


@mock_cognitoidp
def test_admin_list_groups_for_user():
    conn = boto3.client("cognito-idp", "us-west-2")

    user_pool_id = conn.create_user_pool(PoolName=str(uuid.uuid4()))["UserPool"]["Id"]
    group_name = str(uuid.uuid4())
    conn.create_group(GroupName=group_name, UserPoolId=user_pool_id)

    username = str(uuid.uuid4())
    conn.admin_create_user(UserPoolId=user_pool_id, Username=username)

    conn.admin_add_user_to_group(
        UserPoolId=user_pool_id, Username=username, GroupName=group_name
    )

    result = conn.admin_list_groups_for_user(Username=username, UserPoolId=user_pool_id)

    result["Groups"].should.have.length_of(1)
    result["Groups"][0]["GroupName"].should.equal(group_name)


@mock_cognitoidp
def test_admin_list_groups_for_user_ignores_deleted_group():
    conn = boto3.client("cognito-idp", "us-west-2")

    user_pool_id = conn.create_user_pool(PoolName=str(uuid.uuid4()))["UserPool"]["Id"]
    group_name = str(uuid.uuid4())
    conn.create_group(GroupName=group_name, UserPoolId=user_pool_id)
    group_name2 = str(uuid.uuid4())
    conn.create_group(GroupName=group_name2, UserPoolId=user_pool_id)

    username = str(uuid.uuid4())
    conn.admin_create_user(UserPoolId=user_pool_id, Username=username)

    conn.admin_add_user_to_group(
        UserPoolId=user_pool_id, Username=username, GroupName=group_name
    )
    conn.admin_add_user_to_group(
        UserPoolId=user_pool_id, Username=username, GroupName=group_name2
    )
    conn.delete_group(GroupName=group_name, UserPoolId=user_pool_id)

    result = conn.admin_list_groups_for_user(Username=username, UserPoolId=user_pool_id)

    result["Groups"].should.have.length_of(1)
    result["Groups"][0]["GroupName"].should.equal(group_name2)


@mock_cognitoidp
def test_admin_remove_user_from_group():
    conn = boto3.client("cognito-idp", "us-west-2")

    user_pool_id = conn.create_user_pool(PoolName=str(uuid.uuid4()))["UserPool"]["Id"]
    group_name = str(uuid.uuid4())
    conn.create_group(GroupName=group_name, UserPoolId=user_pool_id)

    username = str(uuid.uuid4())
    conn.admin_create_user(UserPoolId=user_pool_id, Username=username)

    conn.admin_add_user_to_group(
        UserPoolId=user_pool_id, Username=username, GroupName=group_name
    )

    result = conn.admin_remove_user_from_group(
        UserPoolId=user_pool_id, Username=username, GroupName=group_name
    )
    list(result.keys()).should.equal(["ResponseMetadata"])  # No response expected
    conn.list_users_in_group(UserPoolId=user_pool_id, GroupName=group_name)[
        "Users"
    ].should.have.length_of(0)
    conn.admin_list_groups_for_user(Username=username, UserPoolId=user_pool_id)[
        "Groups"
    ].should.have.length_of(0)


@mock_cognitoidp
def test_admin_remove_user_from_group_again_is_noop():
    conn = boto3.client("cognito-idp", "us-west-2")

    user_pool_id = conn.create_user_pool(PoolName=str(uuid.uuid4()))["UserPool"]["Id"]
    group_name = str(uuid.uuid4())
    conn.create_group(GroupName=group_name, UserPoolId=user_pool_id)

    username = str(uuid.uuid4())
    conn.admin_create_user(UserPoolId=user_pool_id, Username=username)

    conn.admin_add_user_to_group(
        UserPoolId=user_pool_id, Username=username, GroupName=group_name
    )
    conn.admin_add_user_to_group(
        UserPoolId=user_pool_id, Username=username, GroupName=group_name
    )


@mock_cognitoidp
def test_admin_create_user():
    conn = boto3.client("cognito-idp", "us-west-2")

    username = str(uuid.uuid4())
    value = str(uuid.uuid4())
    user_pool_id = conn.create_user_pool(PoolName=str(uuid.uuid4()))["UserPool"]["Id"]
    result = conn.admin_create_user(
        UserPoolId=user_pool_id,
        Username=username,
        UserAttributes=[{"Name": "thing", "Value": value}],
    )

    result["User"]["Username"].should.equal(username)
    result["User"]["UserStatus"].should.equal("FORCE_CHANGE_PASSWORD")
    result["User"]["Attributes"].should.have.length_of(1)
    result["User"]["Attributes"][0]["Name"].should.equal("thing")
    result["User"]["Attributes"][0]["Value"].should.equal(value)
    result["User"]["Enabled"].should.equal(True)


@mock_cognitoidp
def test_admin_create_existing_user():
    conn = boto3.client("cognito-idp", "us-west-2")

    username = str(uuid.uuid4())
    value = str(uuid.uuid4())
    user_pool_id = conn.create_user_pool(PoolName=str(uuid.uuid4()))["UserPool"]["Id"]
    conn.admin_create_user(
        UserPoolId=user_pool_id,
        Username=username,
        UserAttributes=[{"Name": "thing", "Value": value}],
    )

    caught = False
    try:
        conn.admin_create_user(
            UserPoolId=user_pool_id,
            Username=username,
            UserAttributes=[{"Name": "thing", "Value": value}],
        )
    except conn.exceptions.UsernameExistsException:
        caught = True

    caught.should.be.true


@mock_cognitoidp
def test_admin_resend_invitation_existing_user():
    conn = boto3.client("cognito-idp", "us-west-2")

    username = str(uuid.uuid4())
    value = str(uuid.uuid4())
    user_pool_id = conn.create_user_pool(PoolName=str(uuid.uuid4()))["UserPool"]["Id"]
    conn.admin_create_user(
        UserPoolId=user_pool_id,
        Username=username,
        UserAttributes=[{"Name": "thing", "Value": value}],
    )

    caught = False
    try:
        conn.admin_create_user(
            UserPoolId=user_pool_id,
            Username=username,
            UserAttributes=[{"Name": "thing", "Value": value}],
            MessageAction="RESEND",
        )
    except conn.exceptions.UsernameExistsException:
        caught = True

    caught.should.be.false


@mock_cognitoidp
def test_admin_resend_invitation_missing_user():
    conn = boto3.client("cognito-idp", "us-west-2")

    username = str(uuid.uuid4())
    value = str(uuid.uuid4())
    user_pool_id = conn.create_user_pool(PoolName=str(uuid.uuid4()))["UserPool"]["Id"]

    caught = False
    try:
        conn.admin_create_user(
            UserPoolId=user_pool_id,
            Username=username,
            UserAttributes=[{"Name": "thing", "Value": value}],
            MessageAction="RESEND",
        )
    except conn.exceptions.UserNotFoundException:
        caught = True

    caught.should.be.true


@mock_cognitoidp
def test_admin_get_user():
    conn = boto3.client("cognito-idp", "us-west-2")

    username = str(uuid.uuid4())
    value = str(uuid.uuid4())
    user_pool_id = conn.create_user_pool(PoolName=str(uuid.uuid4()))["UserPool"]["Id"]
    conn.admin_create_user(
        UserPoolId=user_pool_id,
        Username=username,
        UserAttributes=[{"Name": "thing", "Value": value}],
    )

    result = conn.admin_get_user(UserPoolId=user_pool_id, Username=username)
    result["Username"].should.equal(username)
    result["UserAttributes"].should.have.length_of(1)
    result["UserAttributes"][0]["Name"].should.equal("thing")
    result["UserAttributes"][0]["Value"].should.equal(value)


@mock_cognitoidp
def test_admin_get_missing_user():
    conn = boto3.client("cognito-idp", "us-west-2")

    username = str(uuid.uuid4())
    user_pool_id = conn.create_user_pool(PoolName=str(uuid.uuid4()))["UserPool"]["Id"]

    caught = False
    try:
        conn.admin_get_user(UserPoolId=user_pool_id, Username=username)
    except conn.exceptions.UserNotFoundException:
        caught = True

    caught.should.be.true


@mock_cognitoidp
def test_list_users():
    conn = boto3.client("cognito-idp", "us-west-2")

    username = str(uuid.uuid4())
    user_pool_id = conn.create_user_pool(PoolName=str(uuid.uuid4()))["UserPool"]["Id"]
    conn.admin_create_user(UserPoolId=user_pool_id, Username=username)
    result = conn.list_users(UserPoolId=user_pool_id)
    result["Users"].should.have.length_of(1)
    result["Users"][0]["Username"].should.equal(username)

    username_bis = str(uuid.uuid4())
    conn.admin_create_user(
        UserPoolId=user_pool_id,
        Username=username_bis,
        UserAttributes=[{"Name": "phone_number", "Value": "+33666666666"}],
    )
    result = conn.list_users(
        UserPoolId=user_pool_id, Filter='phone_number="+33666666666'
    )
    result["Users"].should.have.length_of(1)
    result["Users"][0]["Username"].should.equal(username_bis)

    # checking Filter with space
    result = conn.list_users(
        UserPoolId=user_pool_id, Filter='phone_number = "+33666666666'
    )
    result["Users"].should.have.length_of(1)
    result["Users"][0]["Username"].should.equal(username_bis)


@mock_cognitoidp
def test_list_users_returns_limit_items():
    conn = boto3.client("cognito-idp", "us-west-2")
    user_pool_id = conn.create_user_pool(PoolName=str(uuid.uuid4()))["UserPool"]["Id"]

    # Given 10 users
    user_count = 10
    for i in range(user_count):
        conn.admin_create_user(UserPoolId=user_pool_id, Username=str(uuid.uuid4()))
    max_results = 5
    result = conn.list_users(UserPoolId=user_pool_id, Limit=max_results)
    result["Users"].should.have.length_of(max_results)
    result.should.have.key("PaginationToken")


@mock_cognitoidp
def test_list_users_returns_pagination_tokens():
    conn = boto3.client("cognito-idp", "us-west-2")
    user_pool_id = conn.create_user_pool(PoolName=str(uuid.uuid4()))["UserPool"]["Id"]

    # Given 10 users
    user_count = 10
    for i in range(user_count):
        conn.admin_create_user(UserPoolId=user_pool_id, Username=str(uuid.uuid4()))

    max_results = 5
    result = conn.list_users(UserPoolId=user_pool_id, Limit=max_results)
    result["Users"].should.have.length_of(max_results)
    result.should.have.key("PaginationToken")

    next_token = result["PaginationToken"]
    result_2 = conn.list_users(
        UserPoolId=user_pool_id, Limit=max_results, PaginationToken=next_token
    )
    result_2["Users"].should.have.length_of(max_results)
    result_2.shouldnt.have.key("PaginationToken")


@mock_cognitoidp
def test_list_users_when_limit_more_than_total_items():
    conn = boto3.client("cognito-idp", "us-west-2")
    user_pool_id = conn.create_user_pool(PoolName=str(uuid.uuid4()))["UserPool"]["Id"]

    # Given 10 users
    user_count = 10
    for i in range(user_count):
        conn.admin_create_user(UserPoolId=user_pool_id, Username=str(uuid.uuid4()))

    max_results = user_count + 5
    result = conn.list_users(UserPoolId=user_pool_id, Limit=max_results)
    result["Users"].should.have.length_of(user_count)
    result.shouldnt.have.key("PaginationToken")


@mock_cognitoidp
def test_admin_disable_user():
    conn = boto3.client("cognito-idp", "us-west-2")

    username = str(uuid.uuid4())
    user_pool_id = conn.create_user_pool(PoolName=str(uuid.uuid4()))["UserPool"]["Id"]
    conn.admin_create_user(UserPoolId=user_pool_id, Username=username)

    result = conn.admin_disable_user(UserPoolId=user_pool_id, Username=username)
    list(result.keys()).should.equal(["ResponseMetadata"])  # No response expected

    conn.admin_get_user(UserPoolId=user_pool_id, Username=username)[
        "Enabled"
    ].should.equal(False)


@mock_cognitoidp
def test_admin_enable_user():
    conn = boto3.client("cognito-idp", "us-west-2")

    username = str(uuid.uuid4())
    user_pool_id = conn.create_user_pool(PoolName=str(uuid.uuid4()))["UserPool"]["Id"]
    conn.admin_create_user(UserPoolId=user_pool_id, Username=username)
    conn.admin_disable_user(UserPoolId=user_pool_id, Username=username)

    result = conn.admin_enable_user(UserPoolId=user_pool_id, Username=username)
    list(result.keys()).should.equal(["ResponseMetadata"])  # No response expected

    conn.admin_get_user(UserPoolId=user_pool_id, Username=username)[
        "Enabled"
    ].should.equal(True)


@mock_cognitoidp
def test_admin_delete_user():
    conn = boto3.client("cognito-idp", "us-west-2")

    username = str(uuid.uuid4())
    user_pool_id = conn.create_user_pool(PoolName=str(uuid.uuid4()))["UserPool"]["Id"]
    conn.admin_create_user(UserPoolId=user_pool_id, Username=username)
    conn.admin_delete_user(UserPoolId=user_pool_id, Username=username)

    caught = False
    try:
        conn.admin_get_user(UserPoolId=user_pool_id, Username=username)
    except conn.exceptions.UserNotFoundException:
        caught = True

    caught.should.be.true


def authentication_flow(conn):
    username = str(uuid.uuid4())
    temporary_password = str(uuid.uuid4())
    user_pool_id = conn.create_user_pool(PoolName=str(uuid.uuid4()))["UserPool"]["Id"]
    user_attribute_name = str(uuid.uuid4())
    user_attribute_value = str(uuid.uuid4())
    client_id = conn.create_user_pool_client(
        UserPoolId=user_pool_id,
        ClientName=str(uuid.uuid4()),
        ReadAttributes=[user_attribute_name],
    )["UserPoolClient"]["ClientId"]

    conn.admin_create_user(
        UserPoolId=user_pool_id,
        Username=username,
        TemporaryPassword=temporary_password,
        UserAttributes=[{"Name": user_attribute_name, "Value": user_attribute_value}],
    )

    result = conn.admin_initiate_auth(
        UserPoolId=user_pool_id,
        ClientId=client_id,
        AuthFlow="ADMIN_NO_SRP_AUTH",
        AuthParameters={"USERNAME": username, "PASSWORD": temporary_password},
    )

    # A newly created user is forced to set a new password
    result["ChallengeName"].should.equal("NEW_PASSWORD_REQUIRED")
    result["Session"].should_not.be.none

    # This sets a new password and logs the user in (creates tokens)
    new_password = str(uuid.uuid4())
    result = conn.respond_to_auth_challenge(
        Session=result["Session"],
        ClientId=client_id,
        ChallengeName="NEW_PASSWORD_REQUIRED",
        ChallengeResponses={"USERNAME": username, "NEW_PASSWORD": new_password},
    )

    result["AuthenticationResult"]["IdToken"].should_not.be.none
    result["AuthenticationResult"]["AccessToken"].should_not.be.none

    return {
        "user_pool_id": user_pool_id,
        "client_id": client_id,
        "id_token": result["AuthenticationResult"]["IdToken"],
        "access_token": result["AuthenticationResult"]["AccessToken"],
        "username": username,
        "password": new_password,
        "additional_fields": {user_attribute_name: user_attribute_value},
    }


@mock_cognitoidp
def test_authentication_flow():
    conn = boto3.client("cognito-idp", "us-west-2")

    authentication_flow(conn)


def user_authentication_flow(conn):
    username = str(uuid.uuid4())
    password = str(uuid.uuid4())
    user_pool_id = conn.create_user_pool(PoolName=str(uuid.uuid4()))["UserPool"]["Id"]
    user_attribute_name = str(uuid.uuid4())
    user_attribute_value = str(uuid.uuid4())
    client_id = conn.create_user_pool_client(
        UserPoolId=user_pool_id,
        ClientName=str(uuid.uuid4()),
        ReadAttributes=[user_attribute_name],
        GenerateSecret=True,
    )["UserPoolClient"]["ClientId"]

    conn.sign_up(
        ClientId=client_id, Username=username, Password=password,
    )

    client_secret = conn.describe_user_pool_client(
        UserPoolId=user_pool_id, ClientId=client_id,
    )["UserPoolClient"]["ClientSecret"]

    conn.confirm_sign_up(
        ClientId=client_id, Username=username, ConfirmationCode="123456",
    )

    # generating secret hash
    key = bytes(str(client_secret).encode("latin-1"))
    msg = bytes(str(username + client_id).encode("latin-1"))
    new_digest = hmac.new(key, msg, hashlib.sha256).digest()
    secret_hash = base64.b64encode(new_digest).decode()

    result = conn.initiate_auth(
        ClientId=client_id,
        AuthFlow="USER_SRP_AUTH",
        AuthParameters={
            "USERNAME": username,
            "SRP_A": str(uuid.uuid4()),
            "SECRET_HASH": secret_hash,
        },
    )

    result = conn.respond_to_auth_challenge(
        ClientId=client_id,
        ChallengeName=result["ChallengeName"],
        ChallengeResponses={
            "PASSWORD_CLAIM_SIGNATURE": str(uuid.uuid4()),
            "PASSWORD_CLAIM_SECRET_BLOCK": result["Session"],
            "TIMESTAMP": str(uuid.uuid4()),
            "USERNAME": username,
        },
    )

    refresh_token = result["AuthenticationResult"]["RefreshToken"]

    # add mfa token
    conn.associate_software_token(
        AccessToken=result["AuthenticationResult"]["AccessToken"],
    )

    conn.verify_software_token(
        AccessToken=result["AuthenticationResult"]["AccessToken"], UserCode="123456",
    )

    conn.set_user_mfa_preference(
        AccessToken=result["AuthenticationResult"]["AccessToken"],
        SoftwareTokenMfaSettings={"Enabled": True, "PreferredMfa": True,},
    )

    result = conn.initiate_auth(
        ClientId=client_id,
        AuthFlow="REFRESH_TOKEN",
        AuthParameters={"SECRET_HASH": secret_hash, "REFRESH_TOKEN": refresh_token,},
    )

    result["AuthenticationResult"]["IdToken"].should_not.be.none
    result["AuthenticationResult"]["AccessToken"].should_not.be.none

    # authenticate user once again this time with mfa token
    result = conn.initiate_auth(
        ClientId=client_id,
        AuthFlow="USER_SRP_AUTH",
        AuthParameters={
            "USERNAME": username,
            "SRP_A": str(uuid.uuid4()),
            "SECRET_HASH": secret_hash,
        },
    )

    result = conn.respond_to_auth_challenge(
        ClientId=client_id,
        ChallengeName=result["ChallengeName"],
        ChallengeResponses={
            "PASSWORD_CLAIM_SIGNATURE": str(uuid.uuid4()),
            "PASSWORD_CLAIM_SECRET_BLOCK": result["Session"],
            "TIMESTAMP": str(uuid.uuid4()),
            "USERNAME": username,
        },
    )

    result = conn.respond_to_auth_challenge(
        ClientId=client_id,
        Session=result["Session"],
        ChallengeName=result["ChallengeName"],
        ChallengeResponses={
            "SOFTWARE_TOKEN_MFA_CODE": "123456",
            "USERNAME": username,
            "SECRET_HASH": secret_hash,
        },
    )

    return {
        "user_pool_id": user_pool_id,
        "client_id": client_id,
        "client_secret": client_secret,
        "secret_hash": secret_hash,
        "id_token": result["AuthenticationResult"]["IdToken"],
        "access_token": result["AuthenticationResult"]["AccessToken"],
        "refresh_token": refresh_token,
        "username": username,
        "password": password,
        "additional_fields": {user_attribute_name: user_attribute_value},
    }


@mock_cognitoidp
def test_user_authentication_flow():
    conn = boto3.client("cognito-idp", "us-west-2")

    user_authentication_flow(conn)


@mock_cognitoidp
def test_token_legitimacy():
    conn = boto3.client("cognito-idp", "us-west-2")

    path = "../../moto/cognitoidp/resources/jwks-public.json"
    with open(os.path.join(os.path.dirname(__file__), path)) as f:
        json_web_key = json.loads(f.read())["keys"][0]

    outputs = authentication_flow(conn)
    id_token = outputs["id_token"]
    access_token = outputs["access_token"]
    client_id = outputs["client_id"]
    issuer = "https://cognito-idp.us-west-2.amazonaws.com/{}".format(
        outputs["user_pool_id"]
    )
    id_claims = json.loads(jws.verify(id_token, json_web_key, "RS256"))
    id_claims["iss"].should.equal(issuer)
    id_claims["aud"].should.equal(client_id)
    id_claims["token_use"].should.equal("id")
    for k, v in outputs["additional_fields"].items():
        id_claims[k].should.equal(v)
    access_claims = json.loads(jws.verify(access_token, json_web_key, "RS256"))
    access_claims["iss"].should.equal(issuer)
    access_claims["aud"].should.equal(client_id)
    access_claims["token_use"].should.equal("access")


@mock_cognitoidp
def test_change_password():
    conn = boto3.client("cognito-idp", "us-west-2")

    outputs = authentication_flow(conn)

    # Take this opportunity to test change_password, which requires an access token.
    newer_password = str(uuid.uuid4())
    conn.change_password(
        AccessToken=outputs["access_token"],
        PreviousPassword=outputs["password"],
        ProposedPassword=newer_password,
    )

    # Log in again, which should succeed without a challenge because the user is no
    # longer in the force-new-password state.
    result = conn.admin_initiate_auth(
        UserPoolId=outputs["user_pool_id"],
        ClientId=outputs["client_id"],
        AuthFlow="ADMIN_NO_SRP_AUTH",
        AuthParameters={"USERNAME": outputs["username"], "PASSWORD": newer_password},
    )

    result["AuthenticationResult"].should_not.be.none


@mock_cognitoidp
def test_change_password__using_custom_user_agent_header():
    # https://github.com/spulec/moto/issues/3098
    # As the admin_initiate_auth-method is unauthenticated, we use the user-agent header to pass in the region
    # This test verifies this works, even if we pass in our own user-agent header
    from botocore.config import Config

    my_config = Config(user_agent_extra="more/info", signature_version="v4")
    conn = boto3.client("cognito-idp", "us-west-2", config=my_config)

    outputs = authentication_flow(conn)

    # Take this opportunity to test change_password, which requires an access token.
    newer_password = str(uuid.uuid4())
    conn.change_password(
        AccessToken=outputs["access_token"],
        PreviousPassword=outputs["password"],
        ProposedPassword=newer_password,
    )

    # Log in again, which should succeed without a challenge because the user is no
    # longer in the force-new-password state.
    result = conn.admin_initiate_auth(
        UserPoolId=outputs["user_pool_id"],
        ClientId=outputs["client_id"],
        AuthFlow="ADMIN_NO_SRP_AUTH",
        AuthParameters={"USERNAME": outputs["username"], "PASSWORD": newer_password},
    )

    result["AuthenticationResult"].should_not.be.none


@mock_cognitoidp
def test_forgot_password():
    conn = boto3.client("cognito-idp", "us-west-2")

    result = conn.forgot_password(ClientId=create_id(), Username=str(uuid.uuid4()))
    result["CodeDeliveryDetails"].should_not.be.none


@mock_cognitoidp
def test_confirm_forgot_password():
    conn = boto3.client("cognito-idp", "us-west-2")

    username = str(uuid.uuid4())
    user_pool_id = conn.create_user_pool(PoolName=str(uuid.uuid4()))["UserPool"]["Id"]
    client_id = conn.create_user_pool_client(
        UserPoolId=user_pool_id, ClientName=str(uuid.uuid4())
    )["UserPoolClient"]["ClientId"]

    conn.admin_create_user(
        UserPoolId=user_pool_id, Username=username, TemporaryPassword=str(uuid.uuid4())
    )

    conn.confirm_forgot_password(
        ClientId=client_id,
        Username=username,
        ConfirmationCode=str(uuid.uuid4()),
        Password=str(uuid.uuid4()),
    )


@mock_cognitoidp
def test_admin_update_user_attributes():
    conn = boto3.client("cognito-idp", "us-west-2")

    username = str(uuid.uuid4())
    user_pool_id = conn.create_user_pool(PoolName=str(uuid.uuid4()))["UserPool"]["Id"]

    conn.admin_create_user(
        UserPoolId=user_pool_id,
        Username=username,
        UserAttributes=[
            {"Name": "family_name", "Value": "Doe"},
            {"Name": "given_name", "Value": "John"},
        ],
    )

    conn.admin_update_user_attributes(
        UserPoolId=user_pool_id,
        Username=username,
        UserAttributes=[
            {"Name": "family_name", "Value": "Doe"},
            {"Name": "given_name", "Value": "Jane"},
        ],
    )

    user = conn.admin_get_user(UserPoolId=user_pool_id, Username=username)
    attributes = user["UserAttributes"]
    attributes.should.be.a(list)
    for attr in attributes:
        val = attr["Value"]
        if attr["Name"] == "family_name":
            val.should.equal("Doe")
        elif attr["Name"] == "given_name":
            val.should.equal("Jane")


@mock_cognitoidp
def test_resource_server():

    client = boto3.client("cognito-idp", "us-west-2")
    name = str(uuid.uuid4())
    value = str(uuid.uuid4())
    res = client.create_user_pool(PoolName=name)

    user_pool_id = res["UserPool"]["Id"]
    identifier = "http://localhost.localdomain"
    name = "local server"
    scopes = [
        {"ScopeName": "app:write", "ScopeDescription": "write scope"},
        {"ScopeName": "app:read", "ScopeDescription": "read scope"},
    ]

    res = client.create_resource_server(
        UserPoolId=user_pool_id, Identifier=identifier, Name=name, Scopes=scopes
    )

    res["ResourceServer"]["UserPoolId"].should.equal(user_pool_id)
    res["ResourceServer"]["Identifier"].should.equal(identifier)
    res["ResourceServer"]["Name"].should.equal(name)
    res["ResourceServer"]["Scopes"].should.equal(scopes)

    with assert_raises(ClientError) as ex:
        client.create_resource_server(
            UserPoolId=user_pool_id, Identifier=identifier, Name=name, Scopes=scopes
        )

    ex.exception.operation_name.should.equal("CreateResourceServer")
    ex.exception.response["Error"]["Code"].should.equal("InvalidParameterException")
    ex.exception.response["Error"]["Message"].should.equal(
        "%s already exists in user pool %s." % (identifier, user_pool_id)
    )
    ex.exception.response["ResponseMetadata"]["HTTPStatusCode"].should.equal(400)


@mock_cognitoidp
def test_sign_up():
    conn = boto3.client("cognito-idp", "us-west-2")
    user_pool_id = conn.create_user_pool(PoolName=str(uuid.uuid4()))["UserPool"]["Id"]
    client_id = conn.create_user_pool_client(
        UserPoolId=user_pool_id, ClientName=str(uuid.uuid4()),
    )["UserPoolClient"]["ClientId"]
    username = str(uuid.uuid4())
    password = str(uuid.uuid4())
    result = conn.sign_up(ClientId=client_id, Username=username, Password=password)
    result["UserConfirmed"].should.be.false
    result["UserSub"].should_not.be.none


@mock_cognitoidp
def test_confirm_sign_up():
    conn = boto3.client("cognito-idp", "us-west-2")
    username = str(uuid.uuid4())
    password = str(uuid.uuid4())
    user_pool_id = conn.create_user_pool(PoolName=str(uuid.uuid4()))["UserPool"]["Id"]
    client_id = conn.create_user_pool_client(
        UserPoolId=user_pool_id, ClientName=str(uuid.uuid4()), GenerateSecret=True,
    )["UserPoolClient"]["ClientId"]
    conn.sign_up(ClientId=client_id, Username=username, Password=password)

    conn.confirm_sign_up(
        ClientId=client_id, Username=username, ConfirmationCode="123456",
    )

    result = conn.admin_get_user(UserPoolId=user_pool_id, Username=username)
    result["UserStatus"].should.equal("CONFIRMED")


@mock_cognitoidp
def test_initiate_auth_USER_SRP_AUTH():
    conn = boto3.client("cognito-idp", "us-west-2")
    username = str(uuid.uuid4())
    password = str(uuid.uuid4())
    user_pool_id = conn.create_user_pool(PoolName=str(uuid.uuid4()))["UserPool"]["Id"]
    client_id = conn.create_user_pool_client(
        UserPoolId=user_pool_id, ClientName=str(uuid.uuid4()), GenerateSecret=True,
    )["UserPoolClient"]["ClientId"]
    conn.sign_up(ClientId=client_id, Username=username, Password=password)
    client_secret = conn.describe_user_pool_client(
        UserPoolId=user_pool_id, ClientId=client_id,
    )["UserPoolClient"]["ClientSecret"]
    conn.confirm_sign_up(
        ClientId=client_id, Username=username, ConfirmationCode="123456",
    )

    key = bytes(str(client_secret).encode("latin-1"))
    msg = bytes(str(username + client_id).encode("latin-1"))
    new_digest = hmac.new(key, msg, hashlib.sha256).digest()
    secret_hash = base64.b64encode(new_digest).decode()

    result = conn.initiate_auth(
        ClientId=client_id,
        AuthFlow="USER_SRP_AUTH",
        AuthParameters={
            "USERNAME": username,
            "SRP_A": str(uuid.uuid4()),
            "SECRET_HASH": secret_hash,
        },
    )

    result["ChallengeName"].should.equal("PASSWORD_VERIFIER")


@mock_cognitoidp
def test_initiate_auth_REFRESH_TOKEN():
    conn = boto3.client("cognito-idp", "us-west-2")
    result = user_authentication_flow(conn)
    result = conn.initiate_auth(
        ClientId=result["client_id"],
        AuthFlow="REFRESH_TOKEN",
        AuthParameters={
            "REFRESH_TOKEN": result["refresh_token"],
            "SECRET_HASH": result["secret_hash"],
        },
    )

    result["AuthenticationResult"]["AccessToken"].should_not.be.none


@mock_cognitoidp
def test_initiate_auth_for_unconfirmed_user():
    conn = boto3.client("cognito-idp", "us-west-2")
    username = str(uuid.uuid4())
    password = str(uuid.uuid4())
    user_pool_id = conn.create_user_pool(PoolName=str(uuid.uuid4()))["UserPool"]["Id"]
    client_id = conn.create_user_pool_client(
        UserPoolId=user_pool_id, ClientName=str(uuid.uuid4()), GenerateSecret=True,
    )["UserPoolClient"]["ClientId"]
    conn.sign_up(ClientId=client_id, Username=username, Password=password)
    client_secret = conn.describe_user_pool_client(
        UserPoolId=user_pool_id, ClientId=client_id,
    )["UserPoolClient"]["ClientSecret"]

    key = bytes(str(client_secret).encode("latin-1"))
    msg = bytes(str(username + client_id).encode("latin-1"))
    new_digest = hmac.new(key, msg, hashlib.sha256).digest()
    secret_hash = base64.b64encode(new_digest).decode()

    caught = False
    try:
        result = conn.initiate_auth(
            ClientId=client_id,
            AuthFlow="USER_SRP_AUTH",
            AuthParameters={
                "USERNAME": username,
                "SRP_A": str(uuid.uuid4()),
                "SECRET_HASH": secret_hash,
            },
        )
    except conn.exceptions.UserNotConfirmedException:
        caught = True

    caught.should.be.true


@mock_cognitoidp
def test_initiate_auth_with_invalid_secret_hash():
    conn = boto3.client("cognito-idp", "us-west-2")
    username = str(uuid.uuid4())
    password = str(uuid.uuid4())
    user_pool_id = conn.create_user_pool(PoolName=str(uuid.uuid4()))["UserPool"]["Id"]
    client_id = conn.create_user_pool_client(
        UserPoolId=user_pool_id, ClientName=str(uuid.uuid4()), GenerateSecret=True,
    )["UserPoolClient"]["ClientId"]
    conn.sign_up(ClientId=client_id, Username=username, Password=password)
    client_secret = conn.describe_user_pool_client(
        UserPoolId=user_pool_id, ClientId=client_id,
    )["UserPoolClient"]["ClientSecret"]
    conn.confirm_sign_up(
        ClientId=client_id, Username=username, ConfirmationCode="123456",
    )

    invalid_secret_hash = str(uuid.uuid4())

    caught = False
    try:
        result = conn.initiate_auth(
            ClientId=client_id,
            AuthFlow="USER_SRP_AUTH",
            AuthParameters={
                "USERNAME": username,
                "SRP_A": str(uuid.uuid4()),
                "SECRET_HASH": invalid_secret_hash,
            },
        )
    except conn.exceptions.NotAuthorizedException:
        caught = True

    caught.should.be.true


@mock_cognitoidp
def test_setting_mfa():
    conn = boto3.client("cognito-idp", "us-west-2")
    result = authentication_flow(conn)
    conn.associate_software_token(AccessToken=result["access_token"])
    conn.verify_software_token(AccessToken=result["access_token"], UserCode="123456")
    conn.set_user_mfa_preference(
        AccessToken=result["access_token"],
        SoftwareTokenMfaSettings={"Enabled": True, "PreferredMfa": True},
    )
    result = conn.admin_get_user(
        UserPoolId=result["user_pool_id"], Username=result["username"]
    )

    result["UserMFASettingList"].should.have.length_of(1)


@mock_cognitoidp
def test_setting_mfa_when_token_not_verified():
    conn = boto3.client("cognito-idp", "us-west-2")
    result = authentication_flow(conn)
    conn.associate_software_token(AccessToken=result["access_token"])

    caught = False
    try:
        conn.set_user_mfa_preference(
            AccessToken=result["access_token"],
            SoftwareTokenMfaSettings={"Enabled": True, "PreferredMfa": True},
        )
    except conn.exceptions.InvalidParameterException:
        caught = True

    caught.should.be.true


@mock_cognitoidp
def test_respond_to_auth_challenge_with_invalid_secret_hash():
    conn = boto3.client("cognito-idp", "us-west-2")
    result = user_authentication_flow(conn)

    valid_secret_hash = result["secret_hash"]
    invalid_secret_hash = str(uuid.uuid4())

    challenge = conn.initiate_auth(
        ClientId=result["client_id"],
        AuthFlow="USER_SRP_AUTH",
        AuthParameters={
            "USERNAME": result["username"],
            "SRP_A": str(uuid.uuid4()),
            "SECRET_HASH": valid_secret_hash,
        },
    )

    challenge = conn.respond_to_auth_challenge(
        ClientId=result["client_id"],
        ChallengeName=challenge["ChallengeName"],
        ChallengeResponses={
            "PASSWORD_CLAIM_SIGNATURE": str(uuid.uuid4()),
            "PASSWORD_CLAIM_SECRET_BLOCK": challenge["Session"],
            "TIMESTAMP": str(uuid.uuid4()),
            "USERNAME": result["username"],
        },
    )

    caught = False
    try:
        conn.respond_to_auth_challenge(
            ClientId=result["client_id"],
            Session=challenge["Session"],
            ChallengeName=challenge["ChallengeName"],
            ChallengeResponses={
                "SOFTWARE_TOKEN_MFA_CODE": "123456",
                "USERNAME": result["username"],
                "SECRET_HASH": invalid_secret_hash,
            },
        )
    except conn.exceptions.NotAuthorizedException:
        caught = True

    caught.should.be.true


# Test will retrieve public key from cognito.amazonaws.com/.well-known/jwks.json,
# which isnt mocked in ServerMode
if not settings.TEST_SERVER_MODE:

    @mock_cognitoidp
    def test_idtoken_contains_kid_header():
        # https://github.com/spulec/moto/issues/3078
        # Setup
        cognito = boto3.client("cognito-idp", "us-west-2")
        user_pool_id = cognito.create_user_pool(PoolName=str(uuid.uuid4()))["UserPool"][
            "Id"
        ]
        client = cognito.create_user_pool_client(
            UserPoolId=user_pool_id,
            ExplicitAuthFlows=[
                "ALLOW_ADMIN_USER_PASSWORD_AUTH",
                "ALLOW_REFRESH_TOKEN_AUTH",
                "ALLOW_ADMIN_NO_SRP_AUTH",
            ],
            AllowedOAuthFlows=["code", "implicit"],
            ClientName=str(uuid.uuid4()),
            CallbackURLs=["https://example.com"],
        )
        client_id = client["UserPoolClient"]["ClientId"]
        username = str(uuid.uuid4())
        temporary_password = "1TemporaryP@ssword"
        cognito.admin_create_user(
            UserPoolId=user_pool_id,
            Username=username,
            TemporaryPassword=temporary_password,
        )
        result = cognito.admin_initiate_auth(
            UserPoolId=user_pool_id,
            ClientId=client_id,
            AuthFlow="ADMIN_NO_SRP_AUTH",
            AuthParameters={"USERNAME": username, "PASSWORD": temporary_password},
        )

        # A newly created user is forced to set a new password
        # This sets a new password and logs the user in (creates tokens)
        password = "1F@kePassword"
        result = cognito.respond_to_auth_challenge(
            Session=result["Session"],
            ClientId=client_id,
            ChallengeName="NEW_PASSWORD_REQUIRED",
            ChallengeResponses={"USERNAME": username, "NEW_PASSWORD": password},
        )
        #
        id_token = result["AuthenticationResult"]["IdToken"]

        # Verify the KID header is present in the token, and corresponds to the KID supplied by the public JWT
        verify_kid_header(id_token)


def verify_kid_header(token):
    """Verifies the kid-header is corresponds with the public key"""
    headers = jwt.get_unverified_headers(token)
    kid = headers["kid"]

    key_index = -1
    keys = fetch_public_keys()
    for i in range(len(keys)):
        if kid == keys[i]["kid"]:
            key_index = i
            break
    if key_index == -1:
        raise Exception("Public key (kid) not found in jwks.json")


def fetch_public_keys():
    keys_url = "https://cognito-idp.{}.amazonaws.com/{}/.well-known/jwks.json".format(
        "us-west-2", "someuserpoolid"
    )
    response = requests.get(keys_url).json()
    return response["keys"]
