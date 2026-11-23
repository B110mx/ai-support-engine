class EngineUnavailableError(RuntimeError):
    """Raised when the requested analysis mode is not registered."""


class EngineExecutionError(RuntimeError):
    """Raised when an engine or external provider cannot complete an analysis."""
