# -*- coding: utf-8 -*-
# Copyright 2022 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Turbinia API - Config router"""

import json
import logging

from fastapi import HTTPException, APIRouter
from fastapi.responses import JSONResponse
from fastapi.requests import Request

from turbinia import config as turbinia_config
from turbinia.api.schemas import request_options

log = logging.getLogger('turbinia')

router = APIRouter(prefix='/config', tags=['Turbinia Configuration'])


@router.get('/')
async def read_config(request: Request):
  """Retrieve turbinia config."""
  try:
    current_config = turbinia_config.toDict()
    if current_config:
      return JSONResponse(content=current_config, status_code=200)
  except (json.JSONDecodeError, TypeError) as exception:
    log.error(f'Error reading configuration: {exception!s}')
    raise HTTPException(
        status_code=500, detail='error reading configuration') from exception


@router.get('/request_options')
async def get_request_options(request: Request):
  """Returns a list BaseRequestOptions attributes."""
  attributes = request_options.BaseRequestOptions.__annotations__
  attributes_dict = {}
  for attribute_name, attribute_type in attributes.items():
    attributes_dict[attribute_name] = {'type': str(attribute_type)}
  return JSONResponse(content=attributes_dict, status_code=200)
