"""Base Agent - Common functionality for all specialized agents."""

from abc import ABC, abstractmethod
from typing import Optional
from smolagents import CodeAgent, InferenceClientModel
from src.tools.code_generation import CODE_GENERATION_TOOLS
from src.utils.logger import log
from src.utils.config import settings


class BaseAgent(ABC):
    """
    Base class for all specialized agents.

    Provides common initialization, model management, and agent creation.
    All specialized agents should inherit from this class.
    """

    def __init__(
        self,
        model: Optional[InferenceClientModel] = None,
        model_id: Optional[str] = None,
        verbose: bool = True
    ):
        """
        Initialize base agent.

        Args:
            model: Shared model instance (preferred for performance)
            model_id: Model ID if creating new model
            verbose: Whether to enable verbose output
        """
        self.model_id = model_id or settings.HF_MODEL
        self.verbose = verbose

        # Use shared model if provided, otherwise create new one
        if model is not None:
            self.model = model
            self._owns_model = False
        else:
            self.model = InferenceClientModel(model_id=self.model_id)
            self._owns_model = True

        # Log initialization
        self._log_initialization()

        # Create agent with tools
        self.agent = self._create_agent()

    def _create_agent(self) -> CodeAgent:
        """
        Create CodeAgent with standard configuration.

        Returns:
            Configured CodeAgent instance
        """
        return CodeAgent(
            tools=CODE_GENERATION_TOOLS,
            model=self.model,
            max_steps=settings.MAX_STEPS,
            # verbose=self.verbose,  # Actually use the verbose parameter!
        )

    @abstractmethod
    def _log_initialization(self):
        """
        Log agent initialization.

        Each specialized agent should implement this to log its own name.
        """
        pass

    def run_task(self, task: str) -> str:
        """
        Run a task using the agent.

        Args:
            task: Task description in natural language

        Returns:
            Task result
        """
        try:
            result = self.agent.run(task)
            return result
        except Exception as e:
            error_msg = f"Task execution failed: {str(e)}"
            log.error(error_msg)
            raise
