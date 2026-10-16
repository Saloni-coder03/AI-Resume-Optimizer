from core.config import settings

class ResumeOptimizerException(Exception):
    status_code: int = 500

    def __init__(self, message: str = "An unexpected error occurred in the Resume Optimizer system."):
        self.message = message
        super().__init__(self.message)

class ResumeParserError(ResumeOptimizerException):
    status_code: int = 422

    def __init__(self, message: str = "Failed to extract text from the resume document."):
        super().__init__(message)

class InvalidFileTypeError(ResumeOptimizerException):
    status_code: int = 400

    def __init__(self, file_extension: str = ""):
        allowed = ", ".join(settings.ALLOWED_EXTENSIONS_LIST)
        message = f"Unsupported file type '{file_extension}'. Only {allowed} formats are permitted."
        super().__init__(message)

class FileTooLargeError(ResumeOptimizerException):
    status_code: int = 413

    def __init__(self, file_size_bytes: int, max_mb: int = None):
        max_mb = max_mb if max_mb is not None else settings.MAX_FILE_SIZE_MB
        message = (
            f"File size ({file_size_bytes / (1024 * 1024):.2f} MB) exceeds "
            f"maximum allowed threshold of {max_mb} MB."
        )
        super().__init__(message)

class ModelLoadError(ResumeOptimizerException):
    status_code: int = 503

    def __init__(self, model_identifier: str = ""):
        message = f"Unable to initialize NLP/ML pipeline model: '{model_identifier}'."
        super().__init__(message)

class MatchingEngineError(ResumeOptimizerException):
    status_code: int = 500

    def __init__(self, message: str = "Error encountered during semantic vector similarity computation."):
        super().__init__(message)

class DatabaseOperationError(ResumeOptimizerException):
    status_code: int = 500

    def __init__(self, message: str = "Database transaction failed."):
        super().__init__(message)