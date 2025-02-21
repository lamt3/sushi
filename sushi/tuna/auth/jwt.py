from datetime import datetime, timedelta


from jose import JWTError, jwt
from tuna.config import Config
from tuna.dtos.member_dto import MemberDTO


def create_jwt_token(member: MemberDTO) -> str:
    """
    Create a JWT access token for the given member
    """
    expire = datetime.utcnow() + timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)
    m = member.to_json()
    m["exp"] = expire
    
    encoded_jwt = jwt.encode(
        m, 
        Config.JWT_SECRET_KEY, 
        algorithm=Config.JWT_ALGORITHM
    )
    
    return encoded_jwt