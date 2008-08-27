from django import forms
from rsvp.models import ATTENDING_CHOICES, Guest


VISIBLE_ATTENDING_CHOICES = [choice for choice in ATTENDING_CHOICES if choice[0] != 'no_rsvp']


class RSVPForm(forms.Form):
    email = forms.EmailField()
    name = forms.CharField(max_length=128)
    attending = forms.ChoiceField(choices=VISIBLE_ATTENDING_CHOICES, initial='yes', widget=forms.RadioSelect)
    number_of_guests = forms.IntegerField(initial=0)
    comment = forms.CharField(max_length=255, required=False, widget=forms.Textarea)
    
    def clean_email(self):
        try:
            guest = Guest.objects.get(email=self.cleaned_data['email'])
        except Guest.DoesNotExist:
            raise forms.ValidationError, 'That e-mail is not on the guest list.'
        
        if guest.attending_status != 'no_rsvp':
            raise forms.ValidationError, 'You have already provided RSVP information.'
        
        return self.cleaned_data['email']
    
    def clean_number_of_guests(self):
        if self.cleaned_data['number_of_guests'] < 0:
            raise forms.ValidationError, "The number of guests you're bringing can not be negative."
        return self.cleaned_data['number_of_guests']
        
    def save(self):
        guest = Guest.objects.get(email=self.cleaned_data['email'])
        
        if self.cleaned_data['name']:
            guest.name = self.cleaned_data['name']
        
        guest.attending_status = self.cleaned_data['attending']
        guest.number_of_guests = self.cleaned_data['number_of_guests']
        guest.comment = self.cleaned_data['comment']
        guest.save()
        return guest
