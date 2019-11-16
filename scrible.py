#!/usr/bin/env python

# make testing faster by doing simple settup here

from app import models
from app import db

s = models.Station.query.first()

s.read_all()
