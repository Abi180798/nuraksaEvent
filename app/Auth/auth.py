import requests

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status

authurl = "https://tahurauser.herokuapp.com/api/v1/auth"
authsuperurl = "{}/authorized_super_admin".format(authurl)
authadminurl = "{}/authorized_admin".format(authurl)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="{}/login".format(authurl))

credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"})

async def get_current_superadmin(token : str = Depends(oauth2_scheme)):
        print(token)
        headers = {'Authorization' : 'Bearer {}'.format(token) }
        print(headers)
        r = requests.get(authsuperurl, headers=headers)
        if r.status_code != status.HTTP_200_OK:
                raise credentials_exception
        return True

async def get_current_admin(token : str = Depends(oauth2_scheme)):
        print(token)
        headers = {'Authorization' : 'Bearer {}'.format(token) }
        print(headers)
        r = requests.get(authadminurl, headers=headers)
        if r.status_code != status.HTTP_200_OK:
                raise credentials_exception
        return True