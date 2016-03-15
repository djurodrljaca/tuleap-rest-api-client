"""
Created on 09.08.2015

:author: Djuro Drljaca

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

import enum

# Public -------------------------------------------------------------------------------------------


class LogicalOperation(enum.Enum):
    And = 0
    Or = 1


class Negation(enum.Enum):
    Disabled = 0
    Enabled = 1


class ComparisonOperation(enum.Enum):
    LessThan = 0
    LessThanOrEqualTo = 1
    EqualTo = 2
    NotEqualTo = 3
    GreaterThanOrEqualTo = 4
    GreaterThan = 5


class StringComparisonOperation(enum.Enum):
    EqualTo = 0
    NotEqualTo = 1
    Contains = 2
    StartsWith = 3
    EndsWith = 4


class CaseSensitivity(enum.Enum):
    CaseSensitive = 0,
    CaseInsensitive = 1


class AbstractFilterItem(object):
    """
    Abstract filter item.
    
    Defines only the object's interface.
    """
    
    def match(self, item):
        """
        Try to match the item to the filter
        
        :param dict item: a dictionary object to match
        
        :return: Success or failure
        :rtype: bool
        """
        raise NotImplementedError()


class NumericFilterItem(AbstractFilterItem):
    """
    Numeric filter item.
    
    Numeric filter item checks if the dictionary object contains a key-value pair that has the
    specified key and also has the value that matches the specified comparison.
    
    :note: Should be used only for dictionary objects that contain some kind of numeric value (for
           example int, float, date, time etc.).
    
    Fields type information:
    :type _key: str
    :type _comparisonOperation: ComparisonOperation
    :type _value: T
    """
    
    def __init__(self, key, comparison_operation, value):
        """
        Constructor
        
        :param str key: key of the dictionary item to filter
        :param ComparisonOperation comparison_operation: Comparison
        :param T value: value of the dictionary item to filter
        """
        self._key = key
        self._comparisonOperation = comparison_operation
        self._value = value
    
    def match(self, item):
        """
        Try to match the item to the filter
        
        :param dict item: a dictionary object to match
        
        :return: Success or failure
        :rtype: bool
        """
        success = False
        value = item[self._key]
        
        # Operation: <
        if self._comparisonOperation == ComparisonOperation.LessThan:
            if value < self._value:
                # match found
                success = True
        # Operation: <=
        elif self._comparisonOperation == ComparisonOperation.LessThanOrEqualTo:
            if value <= self._value:
                # match found
                success = True
        # Operation: ==
        elif self._comparisonOperation == ComparisonOperation.EqualTo:
            if value == self._value:
                # match found
                success = True
        # Operation: !=
        elif self._comparisonOperation == ComparisonOperation.NotEqualTo:
            if value != self._value:
                # match found
                success = True
        # Operation: >=
        elif self._comparisonOperation == ComparisonOperation.GreaterThanOrEqualTo:
            if value >= self._value:
                # match found
                success = True
        # Operation: >
        elif self._comparisonOperation == ComparisonOperation.GreaterThan:
            if value > self._value:
                # match found
                success = True
        else:
            raise Exception("Error: invalid comparison operation!")
        
        return success


class NumericInRangeFilterItem(AbstractFilterItem):
    """
    Numeric in range filter item checks if the dictionary object contains a key-value pair that has
    the specified key and also has a value that is in the specified range.
    
    :note: Should be used only for dictionary objects that contain some kind of numeric value (for
           example int, float, date, time etc.).
    
    Fields type information:
    :type _key: str
    :type _lowerLimit: T
    :type _lowerLimitIncluded: bool
    :type _upperLimit: T
    :type _upperLimitIncluded: bool
    """
    
    def __init__(self,
                 key,
                 lower_limit,
                 lower_limit_included,
                 upper_limit,
                 upper_limit_included):
        """
        
        Constructor
        
        :param str key: key of the dictionary item to filter
        :param T lower_limit: Lower limit
        :param bool lower_limit_included: Is lower limit included
        :param T upper_limit: Upper limit
        :param bool upper_limit_included: Is lower upper included
        """
        self._key = key
        self._lowerLimit = lower_limit
        self._lowerLimitIncluded = lower_limit_included
        self._upperLimit = upper_limit
        self._upperLimitIncluded = upper_limit_included
    
    def match(self, item):
        """
        Try to match the item to the filter
        
        :param dict item: a dictionary object to match
        
        :return: Success or failure
        :rtype: bool
        """
        success = False

        # noinspection PyBroadException,PyBroadException
        try:
            value = item[self._key]
            
            # Check for lower limit
            lower_limit_matched = False
            
            if self._lowerLimitIncluded:
                if self._lowerLimit <= value:
                    lower_limit_matched = True
            else:
                if self._lowerLimit < value:
                    lower_limit_matched = True
            
            # Check for upper limit
            if lower_limit_matched:
                if self._upperLimitIncluded:
                    if value <= self._upperLimit:
                        success = True
                else:
                    if value < self._upperLimit:
                        success = True
        except:
            pass
        
        return success


class NumericOutOfRangeFilterItem(AbstractFilterItem):
    """
    Numeric out of range filter item checks if the dictionary object contains a key-value pair that
    has the specified key and also has a value that is outside the specified range.
    
    :note: Should be used only for dictionary objects that contain some kind of numeric value (for
           example int, float, date, time etc.).
    
    Fields type information:
    :type _inRangeFilter: NumericInRangeFilterItem
    """
    
    def __init__(self,
                 key,
                 lower_limit,
                 lower_limit_included,
                 upper_limit,
                 upper_limit_included):
        """
        
        Constructor
        
        :param str key: key of the dictionary item to filter
        :param T lower_limit: Lower limit
        :param bool lower_limit_included: Is lower limit included
        :param T upper_limit: Upper limit
        :param bool upper_limit_included: Is lower upper included
        """
        self._inRangeFilter = NumericInRangeFilterItem(key,
                                                       lower_limit,
                                                       lower_limit_included,
                                                       upper_limit,
                                                       upper_limit_included)
    
    def match(self, item):
        """
        Try to match the item to the filter
        
        :param dict item: a dictionary object to match
        
        :return: Success or failure
        :rtype: bool
        """
        success = not self._inRangeFilter.match(item)
        
        return success


class StringFilterItem(AbstractFilterItem):
    """
    String filter item.
    
    String filter item checks if the dictionary object contains a key-value pair that has the
    specified key and also has the value that matches the specified comparison.
    
    :note: Should be used only for dictionary objects that contain some kind of numeric value (for
           example int, float, date, time etc.).
    
    Fields type information:
    :type _key: str
    :type _comparisonOperation: StringComparisonOperation
    :type _value: T
    :type _caseSensitive: CaseSensitivity
    """
    
    def __init__(self,
                 key,
                 comparison_operation,
                 value,
                 case_sensitive=CaseSensitivity.CaseSensitive):
        """
        Constructor
        
        :param str key: key of the dictionary item to filter
        :param StringComparisonOperation comparison_operation: Comparison
        :param str value: value of the dictionary item to filter
        :param CaseSensitivity case_sensitive: Case sensitive comparison
        """
        self._key = key
        self._comparisonOperation = comparison_operation
        self._value = value
        self._caseSensitive = case_sensitive
    
    def match(self, item):
        """
        Try to match the item to the filter
        
        :param dict item: a dictionary object to match
        
        :return: Success or failure
        :rtype: bool
        """
        value = item[self._key]
        
        # Handle case sensitivity
        if self._caseSensitive == CaseSensitivity.CaseSensitive:
            str_input_value = value
            str_filter_value = self._value
        elif self._caseSensitive == CaseSensitivity.CaseInsensitive:
            str_input_value = value.lower()
            str_filter_value = self._value.lower()
        else:
            raise Exception("Error: invalid case sensitivity!")
        
        # Operation: Equal to
        if self._comparisonOperation == StringComparisonOperation.EqualTo:
            success = (str_input_value == str_filter_value)
        # Operation: Not equal to
        elif self._comparisonOperation == StringComparisonOperation.NotEqualTo:
            success = (str_input_value != str_filter_value)
        # Operation: Contains
        elif self._comparisonOperation == StringComparisonOperation.Contains:
            success = (str_filter_value in str_input_value)
        # Operation: Starts with
        elif self._comparisonOperation == StringComparisonOperation.StartsWith:
            success = str_input_value.startswith(str_filter_value)
        # Operation: Ends with
        elif self._comparisonOperation == StringComparisonOperation.EndsWith:
            success = str_input_value.endswith(str_filter_value)
        else:
            raise Exception("Error: invalid string comparison operation!")
        
        return success


class FilterQuery(object):
    """
    Filter query
    
    Fields type information:
    :type _queryItems: list[AbstractFilterItem | FilterQuery]
    :type _logicalOperation: LogicalOperation
    :type _negation: Negation
    """
    
    def __init__(self, query_items, logical_operation, negation=Negation.Disabled):
        """
        Constructor
        
        :param query_items: List of any combination of filter items and filter (sub)queries
        :type query_items: list[AbstractFilterItem | FilterQuery]
        :param LogicalOperation logical_operation: logical operation applied to all query items
        :param Negation negation: Enable or disable negation of the complete query
        """
        self._queryItems = query_items
        self._logicalOperation = logical_operation
        self._negation = negation
    
    def execute(self, item):
        """
        execute query
        
        :param dict item: Dictionary object that should be filtered
        
        :return: Query execution result (item either matches or does not match the filter query)
        :rtype: bool
        """
        # execute filter query
        if self._logicalOperation == LogicalOperation.And:
            matches = self._execute_query_with_and_operation(item)
        elif self._logicalOperation == LogicalOperation.Or:
            matches = self._execute_query_with_or_operation(item)
        else:
            raise Exception("Error: invalid logical operation!")
        
        # Check if negation is enabled
        if self._negation == Negation.Enabled:
            matches = (not matches)
        
        return matches
    
    def _execute_query_with_and_operation(self, item):
        """
        execute query on a single dictionary object for a logical AND operation over all query items
        
        :param dict item: Dictionary object that the query is executed on
        
        :return: Query execution result (item either matches or does not match the filter query)
        :rtype: bool
        """
        matches = True
        
        for queryItem in self._queryItems:
            if isinstance(queryItem, AbstractFilterItem):
                #: :type queryItem: AbstractFilterItem
                if not queryItem.match(item):
                    matches = False
                    break
            elif isinstance(queryItem, FilterQuery):
                #: :type queryItem: FilterQuery
                if not queryItem.execute(item):
                    matches = False
                    break
            else:
                raise Exception("Error: invalid query item type!")
        
        return matches
    
    def _execute_query_with_or_operation(self, item):
        """
        execute query on a single dictionary object for a logical OR operation over all query items
        
        :param dict item: Dictionary object that the query is executed on
        
        :return: Query execution result (item either matches or does not match the filter query)
        :rtype: bool
        """
        matches = False
        
        for queryItem in self._queryItems:
            if isinstance(queryItem, AbstractFilterItem):
                #: :type queryItem: AbstractFilterItem
                if queryItem.match(item):
                    matches = True
                    break
            elif isinstance(queryItem, FilterQuery):
                #: :type queryItem: FilterQuery
                if queryItem.execute(item):
                    matches = True
                    break
            else:
                raise Exception("Error: invalid query item type!")
        
        return matches
