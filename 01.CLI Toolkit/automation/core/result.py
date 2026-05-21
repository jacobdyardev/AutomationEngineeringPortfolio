class TaskResult:

    def __init__(
        self,
        success: bool,
        message: str = "",
        artifacts=None,
        partial: bool = False,
    ):
        self.success = success
        self.partial = partial
        self.message = message
        self.artifacts = artifacts or []