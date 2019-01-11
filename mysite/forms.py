from django import forms

class LoginForm(forms.Form):
    email = forms.EmailField(label='courriel')
    password = forms.CharField(label='Mot de passe', widget = forms.PasswordInput)

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            if password != 'sesame' or email != 'bvanbever1@gmail.com':
                raise forms.ValidationError('Adresse de courriel ou mot de passe erroné.')

        return cleaned_data