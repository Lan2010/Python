#!/usr/bin/env python3
#-- coding:utf8 --
'''
Created on 2018年10月9日

@author: dev-lan
'''
class APIError(Exception):

    def __init__(self, error, data='', message=''):
        super(APIError, self).__init__(message)
        self.error = error
        self.data = data
        self.message = message

        
class APIValueError(APIError):

    def __init__(self, field, message=''):
        super(APIValueError, self).__init__('value:invalid', field, message)


class APIResourceNotFoundError(APIError):

        def __init__(self, field, message=''):
            super(APIResourceNotFoundError, self).__init__('value:notfound', field, message)

        
class APIPermissionError(APIError):

    def __init__(self, message=''):
        super(APIPermissionError, self).__init__('permission:forbidden', 'permission', message)