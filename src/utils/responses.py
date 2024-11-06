from pydantic import BaseModel
from starlette import status


class ResponseModel(BaseModel):
    request_id: str = None
    process_time: float = None
    message: str
    status_code: str
    func: str = None


class SuccessResponse(ResponseModel):
    status_code: int = status.HTTP_200_OK
    message: str = "Success"


class ConflictResponse(ResponseModel):
    status_code: int = status.HTTP_409_CONFLICT
    message: str = "Conflict"


class NotFoundResponse(ResponseModel):
    status_code: int = status.HTTP_404_NOT_FOUND
    message: str = "Not Found"


class BadRequestResponse(ResponseModel):
    status_code: int = status.HTTP_400_BAD_REQUEST
    message: str = "Bad Request"


class InternalServerErrorResponse(ResponseModel):
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    message: str = "Internal Server Error"
