from django.utils.translation import ugettext as _
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from rsvp.models import ATTENDING_CHOICES, Guest


VISIBLE_ATTENDING_CHOICES = [choice for choice in ATTENDING_CHOICES if choice[0] != 'no_rsvp']


class RSVPForm(forms.Form):
    email = forms.EmailField()
    name = forms.CharField(max_length=128)
    attending = forms.ChoiceField(choices=VISIBLE_ATTENDING_CHOICES, initial='yes', widget=forms.RadioSelect)
    number_of_guests = forms.IntegerField(initial=0)
    comment = forms.CharField(max_length=255, required=False, widget=forms.Textarea)
    
    def __init__(self, *args, **kwargs):
        if 'guest_class' in kwargs:
            self.guest_class = kwargs['guest_class']
            del(kwargs['guest_class'])
        else:
            self.guest_class = Guest
        super(RSVPForm, self).__init__(*args, **kwargs)
    
    def clean_email(self):
        try:
            guest = self.guest_class._default_manager.get(email=self.cleaned_data['email'])
        except ObjectDoesNotExist:
            raise forms.ValidationError(_('That e-mail is not on the guest list.'), code='not_on_list')
        
        if hasattr(guest, 'attending_status') and guest.attending_status != 'no_rsvp':
            raise forms.ValidationError(_('You have already provided RSVP information.'), code='already_rsvp')
        
        return self.cleaned_data['email']
    
    def clean_number_of_guests(self):
        if self.cleaned_data['number_of_guests'] < 0:
            raise forms.ValidationError(_("The number of guests you're bringing can not be negative."), code='negative_guests')
        return self.cleaned_data['number_of_guests']
        
    def save(self):
        guest = self.guest_class._default_manager.get(email=self.cleaned_data['email'])
        
        if self.cleaned_data['name']:
            guest.name = self.cleaned_data['name']
        
        guest.attending_status = self.cleaned_data['attending']
        guest.number_of_guests = self.cleaned_data['number_of_guests']
        guest.comment = self.cleaned_data['comment']
        guest.save()
        return guest
