from fastapi import Request,Response
from app.logger.logger import logger
import time
async def log_middleware(request : Request, call_next):

    start = time.time()
    response: Response= await call_next(request)
    process_time = time.time() - start

    logger.info(
        f"{request.method} {request.url.path} Status {response.status_code} Time : {process_time}s"
    )


    return response