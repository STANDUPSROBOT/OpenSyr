#!/bin/sh

echo YARN START
cd ./API-Projet-TER/react-flask-app
lxterminal -e sh ./startup.sh &

echo FLASK START

cd ./api
lxterminal -e sh ./startup.sh &