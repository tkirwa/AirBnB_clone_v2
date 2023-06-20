#!/usr/bin/python3
""" Unittests : console """
import json
import os
import sys
import unittest
from io import StringIO
from unittest.mock import patch

import pep8

from console import HBNBCommand


class TestConsole(unittest.TestCase):
    """test console class"""

    def test_all(self):
        """test all method"""
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("all NUGGET")
            self.assertEqual(f.getvalue(), "\n** class doesn't exist **\n")

    def test_show(self):
        """test show method"""
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("show NUGGET")
            self.assertEqual(f.getvalue(), "\n** class doesn't exist **\n")

    def test_create(self):
        """test create method"""
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("create NUGGET")
            self.assertEqual(f.getvalue(), "\n** class doesn't exist **\n")

    def test_update(self):
        """test update method"""
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("update NUGGET")
            self.assertEqual(f.getvalue(), "\n** class doesn't exist **\n")

    def test_destroy(self):
        """test destroy method"""
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("destroy NUGGET")
            self.assertEqual(f.getvalue(), "\n** class doesn't exist **\n")

    def test_destroy(self):
        """test detroy method"""
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("destroy NUGGET")
            self.assertEqual(f.getvalue(), "\n** class doesn't exist **\n")
