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

from enum import IntEnum

# Public -------------------------------------------------------------------------------------------


class FieldsToFetch(IntEnum):
    All = 0
    Comments = 1


class FieldValues(IntEnum):
    No = 0
    All = 1


class FieldValuesFormat(IntEnum):
    No = 0
    Collection = 1
    ByField = 2
    All = 3


class FieldValuesStructure(IntEnum):
    Minimal = 0
    Complete = 1

class Order(IntEnum):
    Ascending = 0
    Descending = 1


class GitFields(IntEnum):
    Basic = 0
    All = 1


class CertificateVerification(IntEnum):
    """
    Certificate verification
    """
    Disabled = 0
    Enabled = 1

