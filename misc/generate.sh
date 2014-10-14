#!/usr/bin/env bash
openssl req -newkey rsa:512 -x509 -days 365 -nodes -out localhost.crt.example -keyout localhost.key.example -batch
