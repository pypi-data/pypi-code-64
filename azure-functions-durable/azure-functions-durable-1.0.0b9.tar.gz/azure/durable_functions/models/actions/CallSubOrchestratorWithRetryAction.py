from typing import Any, Dict, Union, Optional

from .Action import Action
from .ActionType import ActionType
from ..utils.json_utils import add_attrib, add_json_attrib
from json import dumps
from ..RetryOptions import RetryOptions
from azure.functions._durable_functions import _serialize_custom_object


class CallSubOrchestratorWithRetryAction(Action):
    """Defines the structure of the Call SubOrchestrator object."""

    def __init__(self, function_name: str, retry_options: RetryOptions,
                 _input: Optional[Any] = None,
                 instance_id: Optional[str] = None):
        self.function_name: str = function_name
        self._input: str = dumps(_input, default=_serialize_custom_object)
        self.retry_options: RetryOptions = retry_options
        self.instance_id: Optional[str] = instance_id

        if not self.function_name:
            raise ValueError("function_name cannot be empty")

    @property
    def action_type(self) -> int:
        """Get the type of action this class represents."""
        return ActionType.CALL_SUB_ORCHESTRATOR_WITH_RETRY

    def to_json(self) -> Dict[str, Union[str, int]]:
        """Convert object into a json dictionary.

        Returns
        -------
        Dict[str, Union(str, int)]
            The instance of the class converted into a json dictionary
        """
        json_dict: Dict[str, Union[str, int]] = {}
        add_attrib(json_dict, self, 'action_type', 'actionType')
        add_attrib(json_dict, self, 'function_name', 'functionName')
        add_attrib(json_dict, self, '_input', 'input')
        add_json_attrib(json_dict, self, 'retry_options', 'retryOptions')
        add_attrib(json_dict, self, 'instance_id', 'instance_id')
        return json_dict
