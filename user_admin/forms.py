from django import forms
from django.contrib import auth
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(label='用户名', widget=forms.TextInput(attrs={'class':'form-control',
                                                                          'placeholder':'请输入用户名'}))
    password = forms.CharField(label='密码', widget=forms.PasswordInput(attrs={'class':'form-control',
                                                                             'placeholder':'请输入密码'}))
    # 所有验证功能都写到form里：对clean方法重写，加入user验证功能，views里就不需要再验证
    def clean(self):
        try:    # 防止前端输入空格
            username = self.cleaned_data['username']
            password = self.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)
        except:
            raise forms.ValidationError('') # 防止前端输入空格导致500，原因是？？？

        if user is None:
            raise forms.ValidationError('* 用户名或密码不正确')
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data


class RegForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=30, min_length=3,
                               widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'请输入用户名'}))

    password = forms.CharField(label='密码', min_length=3,
                               widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'请输入密码'}))

    password_again = forms.CharField(label='密码', min_length=3,
                                     widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请再次输入密码'}))

    email = forms.EmailField(label='邮箱',
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '请输入邮箱'}))

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户名已存在')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱已存在')
        return email

    def clean_password_again(self):
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']
        if password != password_again:
            raise forms.ValidationError('两次输入的密码不一致')
        return password_again


class ChangeNicknameForm(forms.Form):
     nickname_new = forms.CharField(label='新的昵称', max_length=30, min_length=3,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入新的昵称'}))
     # 接收从views方法中实例化时，传进来的参数user
     def __init__(self, *args, **kwargs):
         if 'user' in kwargs:
             self.user = kwargs.pop('user')
         super(ChangeNicknameForm, self).__init__(*args, **kwargs)
     def clean(self):
         # 判断用户是否登录，未登录不允许修改昵称
         if self.user.is_authenticated:
             self.cleaned_data['user'] = self.user
         else:
             raise forms.ValidationError('用户尚未登录')

     def clean_nickname_new(self):
         nickname_new = self.cleaned_data.get('nickname_new', '').strip()
         if nickname_new == '':
             raise forms.ValidationError('昵称不能为空')
         return nickname_new


class BindEmailForm(forms.Form):
    email = forms.EmailField(label='邮箱',
                               widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '请输入正确的邮箱地址'}))
    verification_code = forms.CharField(label='验证码', required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请点击【发送验证码】验证邮箱有效性'}))

    # 接收从views方法中实例化时，传进来的request参数
    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(BindEmailForm, self).__init__(*args, **kwargs)

    def clean(self):
        # 校验登录态，user信息来自request参数
        if self.request.user.is_authenticated:
            self.cleaned_data['user'] = self.request.user
        else:
            raise forms.ValidationError('用户尚未登录')
        # 判断验证码
        code = self.request.session.get('bind_email_code', '')
        verification_code = self.cleaned_data.get('verification_code', '')
        if not ( code != '' and code == verification_code):
            raise forms.ValidationError('* 验证码不正确')
        return self.cleaned_data


    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('该邮箱已经被使用')
        return email


    def clean_verification_code(self):
        verification_code = self.cleaned_data['verification_code'].strip()
        if verification_code == '':
            raise forms.ValidationError('验证码不能为空')
        return verification_code

