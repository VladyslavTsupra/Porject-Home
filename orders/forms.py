import re

from django import forms


# Checkout form.
class CreateOrderForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    phone_number = forms.CharField()
    requires_delivery = forms.ChoiceField(
        choices=[
            ("0", False),
            ("1", True),
        ],
    )
    delivery_address = forms.CharField(required=False)
    payment_on_get = forms.ChoiceField(
        choices=[
            ("0", False),
            ("1", True),
        ],
    )

    # Checks that the phone number has exactly 10 digits.
    def clean_phone_number(self):
        data = self.cleaned_data["phone_number"]

        if not data.isdigit():
            raise forms.ValidationError("Phone number must contain digits only")

        pattern = re.compile(r"^\d{10}$")
        if not pattern.match(data):
            raise forms.ValidationError("Invalid number format")

        return data
