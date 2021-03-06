# -*- coding: utf-8 -*-
from braces.forms import UserKwargModelFormMixin
from django import forms

from .models import Choice, Condition, Question, Sheet, Answer, AnswerChoice, AnswerText


class RelatedInstanceMixin(object):
    def __init__(self, *args, **kwargs):
        related = kwargs.pop('related', {})
        super(RelatedInstanceMixin, self).__init__(*args, **kwargs)
        for key, value in related.items():
            setattr(self.instance, key, value)


class QuestionForm(UserKwargModelFormMixin, RelatedInstanceMixin, forms.ModelForm):
    class Meta:
        model = Question
        fields = ['name', 'description', 'type', 'count']


class ChoiceForm(RelatedInstanceMixin, forms.ModelForm):

    class Meta:
        model = Choice
        fields = ['key', 'value']


class ConditionForm(RelatedInstanceMixin, forms.ModelForm):
    class Meta:
        model = Condition
        fields = ['type', 'value']


class SheetForm(UserKwargModelFormMixin, RelatedInstanceMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SheetForm, self).__init__(*args, **kwargs)
        self.instance.user = self.user

    class Meta:
        model = Sheet
        fields = ['monitoring_institution']


class AnswerMixin(object):
    def __init__(self, *args, **kwargs):
        self.question = kwargs.pop('question')
        self.sheet = kwargs.pop('sheet')
        super(AnswerMixin, self).__init__(*args, **kwargs)
        self.instance.answer = Answer.objects.create(sheet=self.sheet,
                                                     question=self.question)


class AnswerChoiceForm(AnswerMixin, forms.ModelForm):
    value = forms.ModelChoiceField(queryset=Choice.objects.none(), to_field_name="key")

    def __init__(self, *args, **kwargs):
        super(AnswerChoiceForm, self).__init__(*args, **kwargs)
        self.fields['value'].queryset = Choice.objects.filter(question=self.question).all()

    class Meta:
        model = AnswerChoice
        fields = ['value']


class AnswerTextForm(AnswerMixin, forms.ModelForm):
    class Meta:
        model = AnswerText
        fields = ['value']


def get_form_cls_for_question(question):
    return {question.TYPE.short_text: AnswerTextForm,
            question.TYPE.long_text: AnswerTextForm,
            question.TYPE.choice: AnswerChoiceForm}[question.type]
