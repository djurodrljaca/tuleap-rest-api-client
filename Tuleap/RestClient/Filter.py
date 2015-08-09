'''
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
'''

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
    '''
    Abstract filter item.
    
    Defines only the object's interface.
    '''
    
    def Match(self, item):
        '''
        Try to match the item to the filter
        
        :param dict item: a dictionary object to match
        
        :return: Success or failure
        :rtype: bool
        '''
        raise NotImplementedError()

class NumericFilterItem(AbstractFilterItem):
    '''
    Numeric filter item.
    
    Numeric filter item checks if the dictionary object contains a key-value pair that has the
    specified key and also has the value that matches the specified comparison.
    
    :note: Should be used only for dictionary objects that contain some kind of numeric value (for
           example int, float, date, time etc.).
    
    Fields type information:
    :type _key: str
    :type _comparisonOperation: ComparisonOperation
    :type _value: T
    '''
    
    def __init__(self, key, comparisonOperation, value):
        '''
        Constructor
        
        :param str key: key of the dictionary item to filter
        :param ComparisonOperation comparisonOperation: Comparison
        :param T value: value of the dictionary item to filter
        '''
        self._key = key
        self._comparisonOperation = comparisonOperation
        self._value = value
    
    def Match(self, item):
        '''
        Try to match the item to the filter
        
        :param dict item: a dictionary object to match
        
        :return: Success or failure
        :rtype: bool
        '''
        success = False
        value = item[self._key]
        
        # Operation: <
        if (self._comparisonOperation == ComparisonOperation.LessThan):
            if (value < self._value):
                # Match found
                success = True
        # Operation: <=
        elif (self._comparisonOperation == ComparisonOperation.LessThanOrEqualTo):
            if (value <= self._value):
                # Match found
                success = True
        # Operation: ==
        elif (self._comparisonOperation == ComparisonOperation.EqualTo):
            if (value == self._value):
                # Match found
                success = True
        # Operation: !=
        elif (self._comparisonOperation == ComparisonOperation.NotEqualTo):
            if (value != self._value):
                # Match found
                success = True
        # Operation: >=
        elif (self._comparisonOperation == ComparisonOperation.GreaterThanOrEqualTo):
            if (value >= self._value):
                # Match found
                success = True
        # Operation: >
        elif (self._comparisonOperation == ComparisonOperation.GreaterThan):
            if (value > self._value):
                # Match found
                success = True
        else:
            raise Exception("Error: invalid comparison operation!")
        
        return success

class NumericInRangeFilterItem(AbstractFilterItem):
    '''
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
    '''
    
    def __init__(self,
                 key,
                 lowerLimit,
                 lowerLimitIncluded,
                 upperLimit,
                 upperLimitIncluded):
        '''
        
        Constructor
        
        :param str key: key of the dictionary item to filter
        :param T lowerLimit: Lower limit
        :param bool lowerLimitIncluded: Is lower limit included
        :param T upperLimit: Upper limit
        :param bool upperLimitIncluded: Is lower upper included
        '''
        self._key = key
        self._lowerLimit = lowerLimit
        self._lowerLimitIncluded = lowerLimitIncluded
        self._upperLimit = upperLimit
        self._upperLimitIncluded = upperLimitIncluded
    
    def Match(self, item):
        '''
        Try to match the item to the filter
        
        :param dict item: a dictionary object to match
        
        :return: Success or failure
        :rtype: bool
        '''
        success = False
        
        try:
            value = item[self._key]
            
            # Check for lower limit
            lowerLimitMatched = False
            
            if (self._lowerLimitIncluded):
                if (self._lowerLimit <= value):
                    lowerLimitMatched = True
            else:
                if (self._lowerLimit < value):
                    lowerLimitMatched = True
            
            # Check for upper limit
            if lowerLimitMatched:
                if (self._upperLimitIncluded):
                    if (value <= self._upperLimit):
                        success = True
                else:
                    if (value < self._upperLimit):
                        success = True
        except:
            pass
        
        return success

class NumericOutOfRangeFilterItem(AbstractFilterItem):
    '''
    Numeric out of range filter item checks if the dictionary object contains a key-value pair that
    has the specified key and also has a value that is outside the specified range.
    
    :note: Should be used only for dictionary objects that contain some kind of numeric value (for
           example int, float, date, time etc.).
    
    Fields type information:
    :type _inRangeFilter: NumericInRangeFilterItem
    '''
    
    def __init__(self,
                 key,
                 lowerLimit,
                 lowerLimitIncluded,
                 upperLimit,
                 upperLimitIncluded):
        '''
        
        Constructor
        
        :param str key: key of the dictionary item to filter
        :param T lowerLimit: Lower limit
        :param bool lowerLimitIncluded: Is lower limit included
        :param T upperLimit: Upper limit
        :param bool upperLimitIncluded: Is lower upper included
        '''
        self._inRangeFilter = NumericInRangeFilterItem(key,
                                                       lowerLimit,
                                                       lowerLimitIncluded,
                                                       upperLimit,
                                                       upperLimitIncluded)
    
    def Match(self, item):
        '''
        Try to match the item to the filter
        
        :param dict item: a dictionary object to match
        
        :return: Success or failure
        :rtype: bool
        '''
        success = not self._inRangeFilter.Match(item)
        
        return success

class StringFilterItem(AbstractFilterItem):
    '''
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
    '''
    
    def __init__(self,
                 key,
                 comparisonOperation,
                 value,
                 caseSensitive = CaseSensitivity.CaseSensitive):
        '''
        Constructor
        
        :param str key: key of the dictionary item to filter
        :param StringComparisonOperation comparisonOperation: Comparison
        :param str value: value of the dictionary item to filter
        :param CaseSensitivity caseSensitive: Case sensitieve comparison
        '''
        self._key = key
        self._comparisonOperation = comparisonOperation
        self._value = value
        self._caseSensitive = caseSensitive
    
    def Match(self, item):
        '''
        Try to match the item to the filter
        
        :param dict item: a dictionary object to match
        
        :return: Success or failure
        :rtype: bool
        '''
        success = False
        value = item[self._key]
        
        # Handle case sensitivity
        if self._caseSensitive == CaseSensitivity.CaseSensitive:
            strInputValue = value
            strFilterValue = self._value
        elif self._caseSensitive == CaseSensitivity.CaseInsensitive:
            strInputValue = value.lower()
            strFilterValue = self._value.lower()
        else:
            raise Exception("Error: invalid case sensitivity!")
        
        # Operation: Equal to
        if (self._comparisonOperation == StringComparisonOperation.EqualTo):
            success = (strInputValue == strFilterValue)
        # Operation: Not equal to
        elif (self._comparisonOperation == StringComparisonOperation.NotEqualTo):
            success = (strInputValue != strFilterValue)
        # Operation: Contains
        elif (self._comparisonOperation == StringComparisonOperation.Contains):
            success = (strFilterValue in strInputValue)
        # Operation: Starts with
        elif (self._comparisonOperation == StringComparisonOperation.StartsWith):
            success = strInputValue.startswith(strFilterValue)
        # Operation: Ends with
        elif (self._comparisonOperation == StringComparisonOperation.EndsWith):
            success = strInputValue.endswith(strFilterValue)
        else:
            raise Exception("Error: invalid string comparison operation!")
        
        return success

class FilterQuery(object):
    '''
    Filter query
    
    Fields type information:
    :type _queryItems: list[AbstractFilterItem | FilterQuery]
    :type _logicalOperation: LogicalOperation
    :type _negation: Negation
    '''
    
    def __init__(self, queryItems, logicalOperation, negation = Negation.Disabled):
        '''
        Constructor
        
        :param queryItems: List of any combination of filter items and filter (sub)queries
        :type queryItems: list[AbstractFilterItem | FilterQuery]
        :param LogicalOperation logicalOperation: logical operation applied to all query items
        :param Negation negation: Enable or disable negation of the complete query
        '''
        self._queryItems = queryItems
        self._logicalOperation = logicalOperation
        self._negation = negation
    
    def Execute(self, item):
        '''
        Execute query
        
        :param dict item: Dictionary object that should be filtered
        
        :return: Query execution result (item either matches or does not match the filter query)
        :rtype: bool
        '''
        # Execute filter query
        matches = False 
        
        if (self._logicalOperation == LogicalOperation.And):
            matches = self._ExecuteQueryWithAndOperation(item)
        elif (self._logicalOperation == LogicalOperation.Or):
            matches = self._ExecuteQueryWithOrOperation(item)
        else:
            raise Exception("Error: invalid logical operation!")
        
        # Check if negation is enabled
        if (self._negation == Negation.Enabled):
            matches = (not matches)
        
        return matches
    
    def _ExecuteQueryWithAndOperation(self, item):
        '''
        Execute query on a single dictionary object for a logical AND operation over all query items
        
        :param dict item: Dictionary object that the query is executed on
        
        :return: Query execution result (item either matches or does not match the filter query)
        :rtype: bool
        '''
        matches = True
        
        for queryItem in self._queryItems:
            if isinstance(queryItem, AbstractFilterItem):
                #: :type queryItem: AbstractFilterItem
                if not queryItem.Match(item):
                    matches = False
                    break
            elif isinstance(queryItem, FilterQuery):
                #: :type queryItem: FilterQuery
                if not queryItem.Execute(item):
                    matches = False
                    break
            else:
                raise Exception("Error: invalid query item type!")
        
        return matches
    
    def _ExecuteQueryWithOrOperation(self, item):
        '''
        Execute query on a single dictionary object for a logical OR operation over all query items
        
        :param dict item: Dictionary object that the query is executed on
        
        :return: Query execution result (item either matches or does not match the filter query)
        :rtype: bool
        '''
        matches = False
        
        for queryItem in self._queryItems:
            if isinstance(queryItem, AbstractFilterItem):
                #: :type queryItem: AbstractFilterItem
                if queryItem.Match(item):
                    matches = True
                    break
            elif isinstance(queryItem, FilterQuery):
                #: :type queryItem: FilterQuery
                if queryItem.Execute(item):
                    matches = True
                    break
            else:
                raise Exception("Error: invalid query item type!")
        
        return matches




























        