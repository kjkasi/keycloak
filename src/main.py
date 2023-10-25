from typing import Annotated
import uvicorn
from fastapi import FastAPI, Depends
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


# http://localhost:8085/realms/test/protocol/openid-connect/token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://host.docker.internal:8085/realms/test/protocol/openid-connect/token")
# idp = FastAPIKeycloak(
#     server_url="http://host.docker.internal:8085/auth",
#     client_id="api",
#     client_secret="XXZypkhOPRoaPlWbLb8X8eazMn843alj",
#     admin_client_secret="E6Cn5aM6Z1S5yIrERqLVCjDPOwffRWbX",
#     realm="Test",
#     callback_uri="http://localhost:8081/callback"
# )
# idp.add_swagger_config(app)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")  # Unprotected
def root():
    return 'Hello World'

@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}


# @app.get("/user")  # Requires logged in
# def current_users(user: OIDCUser = Depends(idp.get_current_user())):
#     return user


# @app.get("/admin")  # Requires the admin role
# def company_admin(user: OIDCUser = Depends(idp.get_current_user(required_roles=["admin"]))):
#     return f'Hi admin {user}'


# @app.get("/login")
# def login_redirect():
#     return RedirectResponse(idp.login_uri)


@app.get("/callback")
def callback(session_state: str, code: str):
    return {
        "session_state": session_state,
        "code": code
        }
    #return idp.exchange_authorization_code(session_state=session_state, code=code)  # This will return an access token


if __name__ == '__main__':
    uvicorn.run('app:app', host="127.0.0.1", port=8081)
