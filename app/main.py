import os
import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware
from app.api.users import routes as users

from app.config import config

os.environ["TZ"] = config.APP_TZ
time.tzset()
if not config.testing:
    pass

app = FastAPI(docs_url=config.docs_url)

app.add_middleware(ProxyHeadersMiddleware, trusted_hosts=config.FORWARDED_ALLOW_IPS)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=config.allow_hosts)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


routes: list = [users]

for router_modole in routes:
    app.include_router(router_modole.router, prefix=router_modole.prefix, tags=router_modole.tags)

