class LlmInvokeError(Exception):
    def __init__(self, message: str, module: str = None, function: str = None, **kwargs):
        self.message = message
        self.module = module
        self.function = function
        super().__init__(message)