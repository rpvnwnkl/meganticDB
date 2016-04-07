from django import forms

class SearchDatesForm(forms.Form):
    check_in = forms.DateField(widget=forms.SelectDateWidget)
    check_out = forms.DateField(widget=forms.SelectDateWidget)
    guests = forms.IntegerField(required=True, min_value=1)
    
    def clean(self):
        print('\nclean method now startingi\n')
        cleaned_data = super(SearchDatesForm, self).clean()
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')
        
        if check_in and check_out:
            print('hello')
            if check_in > check_out:
                raise forms.ValidationError(
                        "Check-in and Check-out dates are not possible."
                        )
