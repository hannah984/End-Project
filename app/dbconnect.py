import sqlite3

def dbconnect():
  conn =sqlite3.connect('feedback.db') #connect to the database
  cur = conn.cursor()
  return cur, conn


#this function is created otherwise it would be repeated often in my code