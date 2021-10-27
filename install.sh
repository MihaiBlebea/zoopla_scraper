#!/bin/bash

echo "installing the database"
sqlite3 store.db < ./init.sql