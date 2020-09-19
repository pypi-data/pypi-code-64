from __future__ import unicode_literals

import boto3
import sure  # noqa

from moto import mock_managedblockchain
from . import helpers


@mock_managedblockchain
def test_create_proposal():
    conn = boto3.client("managedblockchain", region_name="us-east-1")

    # Create network
    response = conn.create_network(
        Name="testnetwork1",
        Framework="HYPERLEDGER_FABRIC",
        FrameworkVersion="1.2",
        FrameworkConfiguration=helpers.default_frameworkconfiguration,
        VotingPolicy=helpers.default_votingpolicy,
        MemberConfiguration=helpers.default_memberconfiguration,
    )
    network_id = response["NetworkId"]
    member_id = response["MemberId"]
    network_id.should.match("n-[A-Z0-9]{26}")
    member_id.should.match("m-[A-Z0-9]{26}")

    # Create proposal
    response = conn.create_proposal(
        NetworkId=network_id,
        MemberId=member_id,
        Actions=helpers.default_policy_actions,
    )
    proposal_id = response["ProposalId"]
    proposal_id.should.match("p-[A-Z0-9]{26}")

    # Find in full list
    response = conn.list_proposals(NetworkId=network_id)
    proposals = response["Proposals"]
    proposals.should.have.length_of(1)
    proposals[0]["ProposalId"].should.equal(proposal_id)

    # Get proposal details
    response = conn.get_proposal(NetworkId=network_id, ProposalId=proposal_id)
    response["Proposal"]["NetworkId"].should.equal(network_id)


@mock_managedblockchain
def test_create_proposal_withopts():
    conn = boto3.client("managedblockchain", region_name="us-east-1")

    # Create network
    response = conn.create_network(
        Name="testnetwork1",
        Framework="HYPERLEDGER_FABRIC",
        FrameworkVersion="1.2",
        FrameworkConfiguration=helpers.default_frameworkconfiguration,
        VotingPolicy=helpers.default_votingpolicy,
        MemberConfiguration=helpers.default_memberconfiguration,
    )
    network_id = response["NetworkId"]
    member_id = response["MemberId"]
    network_id.should.match("n-[A-Z0-9]{26}")
    member_id.should.match("m-[A-Z0-9]{26}")

    # Create proposal
    response = conn.create_proposal(
        NetworkId=network_id,
        MemberId=member_id,
        Actions=helpers.default_policy_actions,
        Description="Adding a new member",
    )
    proposal_id = response["ProposalId"]
    proposal_id.should.match("p-[A-Z0-9]{26}")

    # Get proposal details
    response = conn.get_proposal(NetworkId=network_id, ProposalId=proposal_id)
    response["Proposal"]["Description"].should.equal("Adding a new member")


@mock_managedblockchain
def test_create_proposal_badnetwork():
    conn = boto3.client("managedblockchain", region_name="us-east-1")

    response = conn.create_proposal.when.called_with(
        NetworkId="n-ABCDEFGHIJKLMNOP0123456789",
        MemberId="m-ABCDEFGHIJKLMNOP0123456789",
        Actions=helpers.default_policy_actions,
    ).should.throw(Exception, "Network n-ABCDEFGHIJKLMNOP0123456789 not found")


@mock_managedblockchain
def test_create_proposal_badmember():
    conn = boto3.client("managedblockchain", region_name="us-east-1")

    # Create network - need a good network
    response = conn.create_network(
        Name="testnetwork1",
        Framework="HYPERLEDGER_FABRIC",
        FrameworkVersion="1.2",
        FrameworkConfiguration=helpers.default_frameworkconfiguration,
        VotingPolicy=helpers.default_votingpolicy,
        MemberConfiguration=helpers.default_memberconfiguration,
    )
    network_id = response["NetworkId"]

    response = conn.create_proposal.when.called_with(
        NetworkId=network_id,
        MemberId="m-ABCDEFGHIJKLMNOP0123456789",
        Actions=helpers.default_policy_actions,
    ).should.throw(Exception, "Member m-ABCDEFGHIJKLMNOP0123456789 not found")


@mock_managedblockchain
def test_create_proposal_badinvitationacctid():
    conn = boto3.client("managedblockchain", region_name="us-east-1")

    # Must be 12 digits
    actions = {"Invitations": [{"Principal": "1234567890"}]}

    # Create network - need a good network
    response = conn.create_network(
        Name="testnetwork1",
        Framework="HYPERLEDGER_FABRIC",
        FrameworkVersion="1.2",
        FrameworkConfiguration=helpers.default_frameworkconfiguration,
        VotingPolicy=helpers.default_votingpolicy,
        MemberConfiguration=helpers.default_memberconfiguration,
    )
    network_id = response["NetworkId"]
    member_id = response["MemberId"]

    response = conn.create_proposal.when.called_with(
        NetworkId=network_id, MemberId=member_id, Actions=actions,
    ).should.throw(Exception, "Account ID format specified in proposal is not valid")


@mock_managedblockchain
def test_create_proposal_badremovalmemid():
    conn = boto3.client("managedblockchain", region_name="us-east-1")

    # Must be 12 digits
    actions = {"Removals": [{"MemberId": "m-ABCDEFGHIJKLMNOP0123456789"}]}

    # Create network - need a good network
    response = conn.create_network(
        Name="testnetwork1",
        Framework="HYPERLEDGER_FABRIC",
        FrameworkVersion="1.2",
        FrameworkConfiguration=helpers.default_frameworkconfiguration,
        VotingPolicy=helpers.default_votingpolicy,
        MemberConfiguration=helpers.default_memberconfiguration,
    )
    network_id = response["NetworkId"]
    member_id = response["MemberId"]

    response = conn.create_proposal.when.called_with(
        NetworkId=network_id, MemberId=member_id, Actions=actions,
    ).should.throw(Exception, "Member ID format specified in proposal is not valid")


@mock_managedblockchain
def test_list_proposal_badnetwork():
    conn = boto3.client("managedblockchain", region_name="us-east-1")

    response = conn.list_proposals.when.called_with(
        NetworkId="n-ABCDEFGHIJKLMNOP0123456789",
    ).should.throw(Exception, "Network n-ABCDEFGHIJKLMNOP0123456789 not found")


@mock_managedblockchain
def test_get_proposal_badnetwork():
    conn = boto3.client("managedblockchain", region_name="us-east-1")

    response = conn.get_proposal.when.called_with(
        NetworkId="n-ABCDEFGHIJKLMNOP0123456789",
        ProposalId="p-ABCDEFGHIJKLMNOP0123456789",
    ).should.throw(Exception, "Network n-ABCDEFGHIJKLMNOP0123456789 not found")


@mock_managedblockchain
def test_get_proposal_badproposal():
    conn = boto3.client("managedblockchain", region_name="us-east-1")

    # Create network - need a good network
    response = conn.create_network(
        Name="testnetwork1",
        Framework="HYPERLEDGER_FABRIC",
        FrameworkVersion="1.2",
        FrameworkConfiguration=helpers.default_frameworkconfiguration,
        VotingPolicy=helpers.default_votingpolicy,
        MemberConfiguration=helpers.default_memberconfiguration,
    )
    network_id = response["NetworkId"]

    response = conn.get_proposal.when.called_with(
        NetworkId=network_id, ProposalId="p-ABCDEFGHIJKLMNOP0123456789",
    ).should.throw(Exception, "Proposal p-ABCDEFGHIJKLMNOP0123456789 not found")
