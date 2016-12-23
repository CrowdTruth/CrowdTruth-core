import csv
import os
from models.entities import *
from pymodm import connect

# Connect to MongoDB and call the connection "my-app".
connect("mongodb://localhost:27017/crowdtruth", alias="default")

def processFeatures(collection):
	pass
	#print collection
	#Unit.objects.refresh(collection)