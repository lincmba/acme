from django import forms


class CsvImportForm(forms.Form):
    csv_file = forms.FileField(
        required=False, label='Select a file',
        widget=forms.FileInput(attrs={'accept': ".csv"}))
