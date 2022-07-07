import os
from shared.nordigen import NordigenSession
from core import env

session = None

def init_session():
    global session
    session = NordigenSession(env.NORDIGEN_ID, env.NORDIGEN_SECRET)