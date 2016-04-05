"""
Created on 16.03.2016

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

# Public -------------------------------------------------------------------------------------------


class ValueParser(object):
    """
    Parses the artifact values and converts them into strings

    Fields type information:
    :type __item: dict
    :type __label: string
    :type __id: int
    :type __value: string
    :type __links: bool
    :type __valid: bool
    """

    def __init__(self, item):
        """
        Constructor

        :param item: the artifact item to ber parsed
        :type item: dict
        """
        self.__item = item
        self.__value = ""
        self.__label = ""
        self.__id = -1
        self.__links = False
        self.__valid = False
        self.__convert_item_to_string()

    def is_valid(self):
        """
        Check whether the supplied item was convertible to string

        :return: item conversion validity
        :rtype: bool
        """
        return self.__valid

    def is_links(self):
        """
        Check whether the current value item contains artifact links

        :return: True if the current value item contains artifact links
        :rtype: bool
        """
        return self.__links

    def get_value(self):
        """
        Get the string representation of the supplied item

        :return: item string representation
        :rtype: string
        """
        return self.__value

    def get_label(self):
        """
        Get the item label

        :return: item label
        :rtype: string
        """
        return self.__label

    def get_id(self):
        """
        Get the item id

        :return: item id
        :rtype: int
        """
        return self.__id

# Private -------------------------------------------------------------------------------------------

    def __get_aid_item_value(self):
        if "field_id" in self.__item:
            self.__id = self.__item["field_id"]
        else:
            return

        if "label" in self.__item:
            self.__label = self.__item["label"]
        else:
            return

        if "value" in self.__item:
            self.__value = str(self.__item["value"])
        else:
            return

        self.__valid = True

    def __get_string_item_value(self):
        if "field_id" in self.__item:
            self.__id = self.__item["field_id"]
        else:
            return

        if "label" in self.__item:
            self.__label = self.__item["label"]
        else:
            return

        if "value" in self.__item:
            self.__value = self.__item["value"]
        else:
            return

        self.__valid = True

    def __get_text_item_value(self):
        if "field_id" in self.__item:
            self.__id = self.__item["field_id"]
        else:
            return

        if "label" in self.__item:
            self.__label = self.__item["label"]
        else:
            return

        if "value" in self.__item:
            self.__value = self.__item["value"]
        else:
            return

        self.__valid = True

    def __get_subby_item_value(self):
        if "field_id" in self.__item:
            self.__id = self.__item["field_id"]
        else:
            return

        if "label" in self.__item:
            self.__label = self.__item["label"]
        else:
            return

        if "value" in self.__item:
            value_subitem = self.__item["value"]
            if "display_name" in value_subitem:
                self.__value = value_subitem["display_name"]
        else:
            return

        self.__valid = True

    def __get_subon_item_value(self):
        if "field_id" in self.__item:
            self.__id = self.__item["field_id"]
        else:
            return

        if "label" in self.__item:
            self.__label = self.__item["label"]
        else:
            return

        if "value" in self.__item:
            self.__value = self.__item["value"]
        else:
            return

        self.__valid = True

    def __get_lud_item_value(self):
        if "field_id" in self.__item:
            self.__id = self.__item["field_id"]
        else:
            return

        if "label" in self.__item:
            self.__label = self.__item["label"]
        else:
            return

        if "value" in self.__item:
            self.__value = self.__item["value"]
        else:
            return

        self.__valid = True

    def __get_sb_item_value(self):
        if "field_id" in self.__item:
            self.__id = self.__item["field_id"]
        else:
            return

        if "label" in self.__item:
            self.__label = self.__item["label"]
        else:
            return

        if "values" in self.__item:
            value_list = self.__item["values"]
            if len(value_list) > 0:
                if "label" in value_list[0]:
                    self.__value = value_list[0]["label"]
        else:
            return

        self.__valid = True

    def __get_msb_item_value(self):
        if "field_id" in self.__item:
            self.__id = self.__item["field_id"]
        else:
            return

        if "label" in self.__item:
            self.__label = self.__item["label"]
        else:
            return

        if "values" in self.__item:
            val_lst = self.__item["values"]
            first_item = True
            for val_tmp in val_lst:
                if "label" in val_tmp:
                    if first_item:
                        self.__value = val_tmp["label"]
                        first_item = False
                    else:
                        self.__value = self.__value + ", " + val_tmp["label"]
        else:
            return

        self.__valid = True

    def __get_cb_item_value(self):
        if "field_id" in self.__item:
            self.__id = self.__item["field_id"]
        else:
            return

        if "label" in self.__item:
            self.__label = self.__item["label"]
        else:
            return

        if "values" in self.__item:
            val_lst = self.__item["values"]
            first_item = True
            for val_tmp in val_lst:
                if "label" in val_tmp:
                    if first_item:
                        self.__value = val_tmp["label"]
                        first_item = False
                    else:
                        self.__value = self.__value + ", " + val_tmp["label"]
        else:
            return

        self.__valid = True

    def __get_rb_item_value(self):
        if "field_id" in self.__item:
            self.__id = self.__item["field_id"]
        else:
            return

        if "label" in self.__item:
            self.__label = self.__item["label"]
        else:
            return

        if "values" in self.__item:
            value_list = self.__item["values"]
            if len(value_list) > 0:
                if "label" in value_list[0]:
                    self.__value = value_list[0]["label"]
        else:
            return

        self.__valid = True

    def __get_file_item_value(self):
        if "field_id" in self.__item:
            self.__id = self.__item["field_id"]
        else:
            return

        if "label" in self.__item:
            self.__label = self.__item["label"]
        else:
            return

        if "file_descriptions" in self.__item:
            file_list = self.__item["file_descriptions"]
            if len(file_list) > 0:
                if "name" in file_list[0]:
                    self.__value = file_list[0]["name"]
        else:
            return

        self.__valid = True

    def __convert_item_to_string(self):
        if "type" in self.__item:
            value_type = self.__item["type"]
            if value_type == "aid":
                self.__get_aid_item_value()
            elif value_type == "string":
                self.__get_string_item_value()
            elif value_type == "text":
                self.__get_text_item_value()
            elif value_type == "subby":
                self.__get_subby_item_value()
            elif value_type == "subon":
                self.__get_subon_item_value()
            elif value_type == "lud":
                self.__get_lud_item_value()
            elif value_type == "sb":
                self.__get_sb_item_value()
            elif value_type == "msb":
                self.__get_msb_item_value()
            elif value_type == "cb":
                self.__get_cb_item_value()
            elif value_type == "rb":
                self.__get_rb_item_value()
            elif value_type == "file":
                self.__get_file_item_value()
            elif value_type == "art_link":
                self.__links = True
                self.__valid = True
            elif value_type == "cross":
                self.__valid = False
            else:
                self.__value = "Unknown_" + value_type
                self.__valid = True
