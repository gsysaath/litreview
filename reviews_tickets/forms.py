from django.forms import ModelForm, Textarea, HiddenInput

from reviews_tickets.models import Review, Ticket


class TicketForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.Meta.required:
            self.fields[field].required = True

    class Meta:
        model = Ticket
        fields = ('title', 'description', 'image')
        required = ["title"]


class ReviewForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rating'].widget.attrs.update(
            {'max': 5, 'min': 0}
        )
        self.fields['rating'].initial = 0
        # self.fields['rating'].widget = HiddenInput()
        self.fields['body'].widget.attrs['rows'] = 5
        self.fields['body'].widget.attrs['cols'] = 70
        

        for field in self.Meta.required:
            self.fields[field].required = True

    class Meta:
        model = Review
        fields = ('rating', 'headline', 'body')
        required = ['rating', 'headline', 'body']
        widgets = {
          'body': Textarea(),
        }
