import os
from fastapi.security.api_key import APIKeyHeader
from fastapi import Depends, HTTPException, status
import json

auth = APIKeyHeader(
    name="Authorization",
    scheme_name="Bearer",
    description="Value: Bearer {token}",
    auto_error=False,
)

async def authorize_key(bearer_token: str = Depends(auth)):
    api_keys = json.loads(os.getenv('API_KEYS'))
    if bearer_token not in api_keys:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"error": "invalid API key."})
