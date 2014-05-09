 # coding: utf-8
from crispy_forms.layout import Layout


class ExtendedLayout(Layout):

    def remove_layout_object(self, pointer_index):
        """
        Remove a children layout object given by its pointer index.
        It will remove the parent layout if it gets empty

        :param pointer_index: field accessor
        """
        # get parent layout object
        fields = self.fields
        for ind in pointer_index[:-1]:
            fields = fields[ind]

        # remove field
        fields.pop(pointer_index[-1])

        # remove container if it has no more elements
        if not fields:
            self.remove_layout_object(pointer_index[:-1])

    def remove_by_fieldname(self, field_name):
        """
        Remove a field from the layout using its name instead of its index.
        It will also remove the parent layout object if its the unique field in this layout.

        :param field_name: the name of the field to be removed.
        """
        pointers = self.get_field_names()

        for pointer in pointers:
            # pointer is like [[0,1,2], 'field_name1']
            if pointer[1] == field_name:
                self.remove_layout_object(pointer[0])
                break
