#!/usr/bin/env python3
import socket
import os
import sys
import argparse

BUFFSIZE = 2048

def status(s):
	while True:
		#Send ping request to show status
		status_ping = "send-status".encode('utf-8')
		s.send(status_ping)

		msg = s.recv(BUFFSIZE).decode('utf-8')
		print(msg)


def watchlist(s):
	while True:
		#Send ping request to show watchlist
		watchlist_ping = "show-watchlist".encode('utf-8')
		s.send(watchlist_ping)

		msg = s.recv(BUFFSIZE).decode('utf-8')
		print(msg)

def refresh(s):
	while True:
		#Send ping request to refresh watchlist
		refresh_ping = "refresh-list".encode('utf-8')
		s.send(refresh_ping)

def setMAL(s, username, password):
	while True:	
		#Send login credentials to server by prepending login header
		cred = 'login' + username + ':' + password
		s.send(cred.encode('utf-8'))

		msg = s.recv(BUFFSIZE).decode('utf-8')
		print(msg)

parser = argparse.ArgumentParser(description="Command-line interface for Umaru-chan")
parser.add_argument('-s', '--status', help="Displays current status.",action='store_true')
parser.add_argument('-w', '--watchlist', help='Displays current set watchlist', action='store_true')
parser.add_argument('-m', '--mal-id', nargs=2, help="Sets username and password of MyAnimeList account")
parser.add_argument('-r', '--refresh', help="Refreshes database", action='store_true')
args = parser.parse_args()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 6969))

if args.status:
	status(s)
if args.watchlist:
	watchlist(s)
if args.refresh:
	refresh(s)
if args.mal_id != None:
	setMAL(s, args.mal_id[0], args.mal_id[1])