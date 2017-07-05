"""
Created on 15.03.2016

:author: Andrej Nussdorfer

Tuleap REST API Client for Python
Copyright (c) Djuro Drljaca, All rights reserved.

This Python module is free software; you can redistribute it and/or modify it under the terms of the
GNU Lesser General Public License as published by the Free Software Foundation; either version 3.0
of the License, or (at your option) any later version.

This Python module is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with this library. If
not, see <http://www.gnu.org/licenses/>.
"""

from enum import Enum

# Public -------------------------------------------------------------------------------------------


class FieldsToFetch(Enum):
    All = 0,
    Comments = 1


class FieldValues(Enum):
    No = 0
    All = 1


class FieldValuesFormat(Enum):
    No = 0
    Collection = 1
    ByField = 2
    All = 3


class Order(Enum):
    Ascending = 0
    Descending = 1


class GitFields(Enum):
    Basic = 0
    All = 1


class CertificateVerification(Enum):
    """
    Certificate verification
    """
    Disabled = 0
    Enabled = 1


class LinkFollowing(Enum):
    """
    Artifact link following rule
    """
    No = 0
    Forward = 1
    Reverse = 2
    All = 3

