# -*- coding: utf8 -*-
# This file is part of PyBossa.
#
# Copyright (C) 2013 SF Isle of Man Limited
#
# PyBossa is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyBossa is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with PyBossa.  If not, see <http://www.gnu.org/licenses/>.

from sqlalchemy import Integer, Boolean, Unicode, Text, String, BigInteger
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy import event
from werkzeug import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin

from pybossa.core import db
from pybossa.model import DomainObject, make_timestamp, JSONType, make_uuid
from pybossa.model.app import App
from pybossa.model.task_run import TaskRun
from pybossa.model.blogpost import Blogpost




class User(db.Model, DomainObject, UserMixin):
    '''A registered user of the PyBossa system'''

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    created = Column(Text, default=make_timestamp)
    email_addr = Column(Unicode(length=254), unique=True, nullable=False)
    name = Column(Unicode(length=254), unique=True, nullable=False)
    fullname = Column(Unicode(length=500), nullable=False)
    locale = Column(Unicode(length=254), default=u'en', nullable=False)
    api_key = Column(String(length=36), default=make_uuid, unique=True)
    passwd_hash = Column(Unicode(length=254), unique=True)
    admin = Column(Boolean, default=False)
    privacy_mode = Column(Boolean, default=True, nullable=False)
    category = Column(Integer)
    flags = Column(Integer)
    twitter_user_id = Column(BigInteger, unique=True)
    facebook_user_id = Column(BigInteger, unique=True)
    google_user_id = Column(String, unique=True)
    ckan_api = Column(String, unique=True)
    info = Column(JSONType, default=dict)
    age = Column(Integer)
    social = Column(String)
    degree = Column(String)
    city = Column(String)

    ## Relationships
    task_runs = relationship(TaskRun, backref='user')
    apps = relationship(App, backref='owner')
    blogposts = relationship(Blogpost, backref='owner')


    def get_id(self):
        '''id for login system. equates to name'''
        return self.name


    def set_password(self, password):
        self.passwd_hash = generate_password_hash(password)


    def check_password(self, password):
        # OAuth users do not have a password
        if self.passwd_hash:
            return check_password_hash(self.passwd_hash, password)
        else:
            return False


    @classmethod
    def by_name(cls, name):
        '''Lookup user by (user)name.'''
        return db.session.query(User).filter_by(name=name).first()


@event.listens_for(User, 'before_insert')
def make_admin(mapper, conn, target):
    users = conn.scalar('select count(*) from "user"')
    if users == 0:
        target.admin = True
