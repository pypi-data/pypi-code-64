# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------


class AzureMLErrorStrings:
    """
    All un-formatted error strings that accompany the common error codes in AzureML.
    """

    class UserErrorStrings:
        """
        Un-formatted error string for all UserErrors.

        Dev note: Please keep this list sorted on keys.
        """
        ARGUMENT_BLANK_OR_EMPTY = "An empty value for argument [{argument_name}] is provided."
        ARGUMENT_INVALID = "Argument [{argument_name}] is of invalid type. Expected type: [{expected_type}]"
        ARGUMENT_MISMATCH = "Argument(s) [{argument_names}] has incompatible values: [{value_list}]."
        ARGUMENT_OUT_OF_RANGE = "Value for argument [{argument_name}] is out of range (Range: [{min} - {max}])."
        AUTH = "Access to resource [{resource_name}] is prohibited. Please make sure the resource exists, " \
               "and/or you have the right permissions on it."
        AUTHENTICATION = "Authentication for [{resource_name}] failed. Please make sure the resource exists, " \
                         "and/or you have the right permissions on it."
        AUTHORIZATION = "Authorization for [{resource_name}] failed. Please make sure the resource exists, " \
                        "and/or you have the right permissions on it."
        BAD_ARGUMENT = "An invalid value for argument [{argument_name}] was provided."
        BAD_DATA = "[{data_argument_name}] was invalid."
        COMPUTE_NOT_FOUND = "Compute [{compute_name}] was not found in workspace [{workspace_name}]."
        CONFLICT = "[{resource_name}] is in a conflicting state."
        CONNECTION_FAILURE = "Connection to [{resource_name}] failed."
        DEPRECATED = "[{feature_name}] is deprecated."
        DISABLED = "[{resource_name}] is disabled."
        DUPLICATE_ARGUMENT = "Argument [{argument_name}] has duplicate values: [{values}]."
        EMPTY_DATA = "[{data_argument_name}] was invalid."
        EXPERIMENT_NOT_FOUND = "Experiment [{experiment_name}] was not found in workspace [{workspace_name}]."
        IMMUTABLE = "[{resource_name}] cannot be modified because it's immutable."
        INVALID_DATA = "[{data_argument_name}] is invalid."
        INVALID_DIMENSION = "[{data_argument_name}] dimension does not have required dimensions."
        KEY_VAULT_NOT_FOUND = "KeyVault [{keyvault_name}] is not found in workspace [{workspace_name}]."
        MALFORMED_ARGUMENT = "Argument [{argument_name}] is malformed."
        MEMORY = "Insufficient memory to execute the request. Please retry on a virtual machine with more memory."
        MISSING_DATA = "[{data_argument_name}] has missing data."
        NOT_FOUND = "Resource [{resource_name}] was not found."
        NOT_READY = "[{resource_name}] is not ready."
        NOT_SUPPORTED = "Request for [{scenario_name}] is not supported."
        QUOTA_EXCEEDED = "Quota exceeded for [{resource_name}]."
        RESOURCE_EXHAUSTED = "Insufficient resource for [{resource_name}] to execute the request."
        STORAGE_ACCOUNT_NOT_FOUND = "Storage account [{storage_account_name}] was not found in workspace " \
                                    "[{workspace_name}]."
        TIMEOUT = "Operation timed out."
        TOO_MANY_REQUESTS = "Received too many requests in a short amount of time. Please retry again later."
        WORKSPACE_NOT_FOUND = "Workspace [{workspace_name}] was not found."

    class SystemErrorStrings:
        """
        Un-formatted error string for all SystemErrors.

        Dev note: Please keep this list sorted on keys.
        """
        CLIENT_ERROR = "Failed to process request. If you think this is a bug, " \
                       "please create a support request quoting client unique identifier [{client_request_id}]"
        SERVICE_ERROR = "Failed to process request. If you think this is a bug, " \
                        "please create a support request quoting service unique identifier [{server_request_id}]"
