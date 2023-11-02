"""
app.py
-------
Quart App file
"""

import sys
from quart import Quart, render_template, redirect

#DON'T GENERATE __PYCACHE__
sys.dont_write_bytecode = True

#FLASK APP
app = Quart(__name__)

@app.route("/")
async def pageHome():
    return await render_template('index.html')

@app.route("/invite")
async def pageHome():
    return await redirect('https://discord.com/api/oauth2/authorize?client_id=1168950370580578385&permissions=0&scope=applications.commands%20bot')
