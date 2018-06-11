from django import forms

class UserForm(forms.Form):
    equation=forms.CharField(label="Рівняння",initial="1/3Cr2O3+1C=2/3Cr+1CO(g)",widget=forms.TextInput(attrs={"class":"upperfield"}))
    t_start=forms.IntegerField(label="Початкова температура у Кельвінах",initial=773,widget=forms.NumberInput(attrs={"class":"lowerfield"}))
    t_stop=forms.IntegerField(label="Кінцева температура",initial=1573,widget=forms.NumberInput(attrs={"class":"lowerfield"}))
    t_step=forms.IntegerField(label="Шаг для температури",initial=50,widget=forms.NumberInput(attrs={"class":"lowerfield"}))