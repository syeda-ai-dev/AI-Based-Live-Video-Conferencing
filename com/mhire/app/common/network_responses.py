import time

class NetworkResponse:
    def _init_(self, version=0.1):
        self.version = version

    def success_response(self, http_code, data, resource, start_time):
        return {
            "code": http_code,
            "message": "Success",
            "meta": {
                "result": round((time.time() - start_time) * 1000),
                "version": self.version,
                "resource": resource
            },
            "data": data
        }

    def error_response(self, http_code, error_code, error_message, resource, start_time):
        return {
            "code": http_code,
            "message": "Fail",
            "error": {
                "code": error_code,
                "message": error_message
            },
            "meta": {
                "result": round((time.time() - start_time) * 1000),
                "version": self.version,
                "resource": resource
            },
        }

class HTTPCode:
    SUCCESS = 200
    NOT_FOUND = 404
    UNPROCESSABLE_ENTITY = 422
    INTERNAL_SERVER_ERROR = 500

class ErrorCode:
    class NotFound:
        REPORT_NOT_FOUND = 40400
        USER_NOT_FOUND = 40401

    class UnprocessableEntity:
        INVALID_INPUT = 42200

    class InternalServerError:
        UNEXPECTED_ERROR = 50000
        SURVEILLANCE_FAILURE = 50001  # Specific to your agents
        ATTRIBUTION_FAILURE = 50002
        ANALYSIS_FAILURE = 50003
        REDTEAM_FAILURE = 50004
        TRANSLATION_FAILURE = 50005
            
class Message:
    class SuccessMessage:
            SOMETHING_SUCCESS = "Something is successful."
    class ErrorMessage:
        REPORT_NOT_FOUND = "Report not found"
        UNEXPECTED_ERROR = "An unexpected error occurred"
        SURVEILLANCE_FAILURE = "Threat detection failed"
        ATTRIBUTION_FAILURE = "Source credibility check failed"
        ANALYSIS_FAILURE = "Risk assessment error"
        REDTEAM_FAILURE = "Adversarial simulation failed"
        TRANSLATION_FAILURE = "Translation pipeline error"