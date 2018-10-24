import base64
import json
from unittest.mock import Mock, patch

from tornado.web import Application
from tornado.testing import AsyncHTTPTestCase

from integration.handlers import ImportClientJsonHandler

from tests import setup_future


class ImportClientJsonHandlerTestCase(AsyncHTTPTestCase):
   pass
