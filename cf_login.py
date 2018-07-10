import os
import random
import getpass
from robobrowser import RoboBrowser

root = '7'

def get_secret(inclupass):
	handle = None
	password = None
	secret_loc = os.path.join(os.path.dirname(__file__), "secret")
	if os.path.isfile(secret_loc):
		secretfile = open(secret_loc, "r")
		rawdata = secretfile.read().rstrip('\n').split()
		handle = (rawdata[0])
		if inclupass:
			password = (rawdata[1])
		secretfile.close()
	if inclupass:
		return handle, password
	else:
		return handle

""" set login """
def set_login(handle=None):
	if handle is None:
		handle = input("Handle: ")
	password = getpass.getpass("Password: ")

	browser = RoboBrowser(parser = "lxml")
	browser.open("http://codeforces.com/enter")
	enter_form = browser.get_form("enterForm")
	enter_form["handleOrEmail"] = handle
	enter_form["password"] = password
	browser.submit_form(enter_form)

	checks = list(map(lambda x: x.getText()[1:].strip(), 
		browser.select("div.caption.titled")))
	if handle not in checks:
		print("Login Failed.")
		return
	else:
		secret_loc = os.path.join(os.path.dirname(__file__), "secret")
		secretfile = open(secret_loc, "w")
		secretfile.write((handle) + " " + (password))
		secretfile.close()
		print("Successfully logged in as " + handle)

""" login """
def login():
	handle, password = get_secret(True)

	browser = RoboBrowser(parser = "lxml")
	browser.open("http://codeforces.com/enter")
	enter_form = browser.get_form("enterForm")
	enter_form["handleOrEmail"] = handle
	enter_form["password"] = password
	browser.submit_form(enter_form)

	checks = list(map(lambda x: x.getText()[1:].strip(), browser.select("div.caption.titled")))
	if handle not in checks:
		print("Login Corrupted.")
		return None
	else:
		return browser

