# -*- coding: utf-8 -*-

from django import forms
from extended_choices import Choices

class NamedExtendedChoiceFormField(forms.Field):
    """
    Special fields, where the values are the constants names instead of the
    integer (could be usefull for example for an API).
    Should not be very userfull in normal HTML form life, but we need one because
    we use forms to do REST parameters validation.
    """
    def __init__(self, choices=(), required=True, widget=None, label=None,
                 initial=None, help_text=None, *args, **kwargs):
        """
        Choices must be instance of ``extended_choices.Choice``.
        """
        super(NamedExtendedChoiceFormField, self).__init__(required=required,
               widget=widget, label=label, initial=initial, help_text=help_text,
               *args, **kwargs)
        if not isinstance(choices, Choices):
            raise ValueError("choices must be an instance of extended_choices.Choices")
        self.choices = choices

    def to_python(self, value):
        """
        Convert the named value to the internal integer.
        """
        # is_required is checked in validate
        if value is None: return None
        if not isinstance(value, (str, unicode)):
            raise forms.ValidationError("Invalid value format.")
        try:
            final = getattr(self.choices, value.upper())
        except AttributeError:
            raise forms.ValidationError("Invalid value.")
        return final


class ExtendedChoiceField(forms.ChoiceField):

    def __init__(self, extended_choices=None, *args, **kwargs):
        if not isinstance(extended_choices, Choices):
            raise TypeError('extended_choices argument to %s is not a Choices instance' % (self, ))
        kwargs['choices'] = extended_choices.CHOICES
        super(ExtendedChoiceField, self).__init__(*args, **kwargs)
        self.extended_choices = extended_choices
        self.value_for_display = None

    def get_value_display(self):
        """
        Display human-readable value corresponding to the value that was
        clean()ed last.

        Returns None if the value doesn't match any choice or if the field has
        not been cleaned yet
        """
        return self.value_for_display

    def clean(self, value):
        rval = super(ExtendedChoiceField, self).clean(value)
        self.value_for_display = self.extended_choices.CHOICES_DICT.get(rval, None)
        return rval


class ExtendedTypedChoiceField(ExtendedChoiceField, forms.TypedChoiceField):
    pass


class MultipleChoiceField(ExtendedChoiceField, forms.MultipleChoiceField):
    pass


class TypedMultipleChoiceField(ExtendedChoiceField, forms.TypedMultipleChoiceField):
    pass
