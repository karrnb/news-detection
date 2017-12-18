from flask import Blueprint
services = Blueprint('services', __name__)

from .naive_bayes import *
from .word_cloud import *
