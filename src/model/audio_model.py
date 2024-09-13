from typing import Optional

from pydantic import Base64Bytes, Base64Str, BaseModel, HttpUrl


class AudioUrl(BaseModel):
    url: HttpUrl

class AudioBase64(BaseModel):
    base64_bytes: Base64Bytes
    base64_str: Optional[Base64Str] = None