from django import forms

from mayan.apps.views.forms import DetailForm

from .models import Theme, UserThemeSetting


class ThemeForm(forms.ModelForm):
    class Meta:
        fields = ('label','font','color_font_header','menu_text_color','background_color_header','background_color_menu','background_color_header_panel',
        'background_website','background_menu_dropdown','btn_color_primary','btn_color_danger','btn_color_success','btn_color_default',
        'font_size_menu','font_size_content_title')
        model = Theme


class UserThemeSettingForm(forms.ModelForm):
    class Meta:
        fields = ('theme',)
        model = UserThemeSetting
        widgets = {
            'theme': forms.Select(
                attrs={
                    'class': 'select2'
                }
            ),
        }


class UserThemeSettingForm_view(DetailForm):
    class Meta:
        fields = ('theme',)
        model = UserThemeSetting