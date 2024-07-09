#!/usr/bin/env python3
""" Module of Auth config
"""
from flask import request
from typing import (
    List,
    TypeVar as TypeVar
)
import fnmatch


class Auth():
    """ Auth class for managing API authentication
    """
    def __init__(self) -> None:
        """ Initialize the Auth class
        """
        pass

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Determines if authentication is required
        based on the path and excluded paths.

        Args:
            path (str): The path to check.
            excluded_paths (List[str]): List of paths
            that do not require authentication.

        Returns:
            bool: True if authentication is required,
            False otherwise.
        """
        if path is None or excluded_paths is None or excluded_paths == []:
            return True

        l_path = len(path)
        if l_path == 0:
            return True

        slash_path = True if path[l_path - 1] == '/' else False

        tmp_path = path
        if not slash_path:
            tmp_path += '/'

        for excluded_path in excluded_paths:
            l_excluded_path = len(excluded_path)
            if l_excluded_path == 0:
                continue

            if excluded_path[l_excluded_path - 1] != '*':
                if tmp_path == excluded_path:
                    return False
            else:
                if excluded_path[:-1] == path[:l_excluded_path - 1]:
                    return False

        return True

    def authorization_header(self, request=None) -> str:
        """ Retrieves the authorization header from the request.

        Args:
            request (flask.Request, optional): The request object.
            Defaults to None.

        Returns:
            str: The authorization header if present,
            None otherwise.
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Retrieves the current user from the request.

        Args:
            request (flask.Request, optional): The request object.
            Defaults to None.

        Returns:
            TypeVar('User'): The current user,
            or None if no user is authenticated.
        """
        return None
