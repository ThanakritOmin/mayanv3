from django.apps import apps
from django.conf import settings
from django.contrib.auth import get_user_model
from django.template import Library
from django.template.exceptions import TemplateDoesNotExist
from django.template.loader import get_template
from django.utils.module_loading import import_string
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from ..literals import COMMENT_APP_TEMPLATE_CACHE_DISABLE

from mayan.apps.appearance.models import UserThemeSetting, Theme

app_templates_cache = {}
register = Library()


@register.simple_tag(takes_context=True)
def appearance_app_templates(context, template_name):
    """
    Fetch the app templates for the requested `template_name`, render it with
    the current `request` from the `context`, and cache it for future use
    unless the template has the no caching comment.
    """
    result = []

    for app in apps.get_app_configs():
        template_id = '{}.{}'.format(app.label, template_name)
        if template_id not in app_templates_cache or settings.DEBUG:
            try:
                app_template = get_template(
                    '{}/app/{}.html'.format(app.label, template_name)
                )
                app_template_output = app_template.render(
                    request=context.get('request')
                )

                if COMMENT_APP_TEMPLATE_CACHE_DISABLE not in app_template.template.source:
                    app_templates_cache[template_id] = app_template_output
            except TemplateDoesNotExist:
                """
                Non fatal just means that the app did not defined an app
                template of this name and purpose.
                """
                app_templates_cache[template_id] = ''
                app_template_output = ''
        else:
            app_template_output = app_templates_cache[template_id]

        result.append(app_template_output)

    return mark_safe(' '.join(result))


@register.filter
def appearance_get_choice_value(field):
    try:
        return dict(field.field.choices)[field.value()]
    except TypeError:
        return ', '.join([subwidget.data['label'] for subwidget in field.subwidgets if subwidget.data['selected']])
    except KeyError:
        return _('None')


@register.filter
def appearance_get_form_media_js(form):
    return [form.media.absolute_path(path) for path in form.media._js]


@register.simple_tag
def appearance_get_icon(icon_path):
    return import_string(dotted_path=icon_path).render()


@register.simple_tag
def appearance_get_user_theme_stylesheet(user):
    #user
    User = get_user_model()
    print("user__now")
    print(user)
    into = user
    #print(type(str(into)))
    #thm = UserThemeSetting.objects.values()
    thm = UserThemeSetting.objects.filter(user_id=1)
    print(thm.values())
    item_theme_setting = thm.values()
    print('End')
    if len(list(item_theme_setting)) == 0 :
        return ''
    tt =  item_theme_setting[0]
    theme_id_ = tt['theme_id']
    print(theme_id_)
    if tt['theme_id'] == None :
        print('Think true')
        return ''
    else :
        stl = Theme.objects.filter(id=theme_id_)
        styy = stl.values()
        stmp = styy[0]
        style = '*{ font-family: '+ str(stmp['font']) +'} \n '+ '.navbar.navbar-default.navbar-fixed-top{  background-color : '+ str(stmp['background_color_header']) + '} \n ' + '#accordion-sidebar .panel-heading{ background-color : ' + str(stmp['background_color_menu']) + '} \n ' + '#menu-main{ background-color : ' + str(stmp['background_color_menu']) + '} \n ' + 'h3#content-title,h4, p small, p.small, .well label:not(.btn), .well td:not(.last), .well li::marker,li,th,.form-group{ color : ' + str(stmp['color_font_header']) + '} \n ' + '.panel-primary &gt; .panel-heading{ background-color : ' + str(stmp['background_color_header_panel']) + '} \n ' + '.navbar-default .navbar-nav&gt;.open&gt;a{ background-color : ' + str(stmp['background_color_header']) + '} \n ' + 'body{ background-color : ' + str(stmp['background_website']) + '} \n ' + '#accordion-sidebar .panel-body{ background-color : ' + str(stmp['background_menu_dropdown']) + '} \n '+ '.btn-primary{ background-color : ' + str(stmp['btn_color_primary']) + '} \n ' + '.btn-danger{ background-color : ' + str(stmp['btn_color_danger']) + '} \n ' + '.btn-success{ background-color : ' + str(stmp['btn_color_success']) + '} \n ' + '.btn-default{ background-color : ' + str(stmp['btn_color_default']) + '} \n' + '.navbar-brand{ fontSize : ' + str(stmp['font_size_header']) + 'px } \n ' + '#accordion-sidebar .panel-title{ fontSize : ' + str(stmp['font_size_menu']) + 'px } \n ' + '#content-title{ fontSize : ' + str(stmp['font_size_content_title']) + 'px } \n ' + '#accordion-sidebar .panel-title{ color : ' + str(stmp['menu_text_color'])+'; \n fontSize: '+str(stmp['font_size_menu'])+'px;' + ' } \n' + '#accordion-sidebar .panel-body a{ color : ' + str(stmp['menu_text_color']) + '} \n'+'.navbar-default .navbar-nav&gt;.open&gt;a,.navbar-default .navbar-nav&gt;.open&gt;a:hover,.navbar-default .navbar-nav&gt;.open&gt;a:focus{  background-color: '+ str(stmp['background_color_header'])+'} \n'+'.navbar.navbar-default.navbar-fixed-top li.dropdown a.dropdown-toggle, li a svg.fa-bell,svg.fa-inbox{ color: '+str(stmp['menu_text_color'])+'} \n'
        print(style)
        print('Real!!!')
        return style
    #print(4)
    #print(thm)
    #print(thm[:])
    #for i in thm:
    #    if i['user_id'] == 1 :
    #        tmp_theme = i['theme_id']
    #    print(i['user_id'])
    #stl = Theme.objects.values()
    #for i in stl:
    #    if i['id'] == tmp_theme:
    #        sstl = i
    #return sstl['stylesheet']
    #return ''
    #User = get_user_model()

    #if user and user.is_authenticated:
    #    try:
    #        theme = user.theme_settings.theme
    #    except User.theme_settings.RelatedObjectDoesNotExist:
            # User had a setting assigned which was later deleted.
    #        return ''
    #    else:
    #        if theme:
    #            return user.theme_settings.theme.stylesheet

    #return ''
@register.simple_tag
def get_font_link():
    #obj = Theme.objects.all().order_by('id')[:1][0]
    thm = UserThemeSetting.objects.filter(user_id=1)  
    item_theme_setting = thm.values()
    # tt =  item_theme_setting[0]
    try:
        tt =  item_theme_setting[0]
        theme_id_ = tt['theme_id']
        stl = Theme.objects.filter(id=theme_id_)
        styy = stl.values()
        stmp = styy[0]
    
        fontRaw = fontname
        fontLink = fontRaw.replace(" ", "+")
        return stmp['font']
    except :
        return ''
    

@register.simple_tag
def appearance_get_user_theme_script():
    obj = UserThemeSetting.objects.filter(user_id=1)
    item_theme_setting = obj.values()
    try:
        tt =  item_theme_setting[0]
        theme_id_ = tt['theme_id']
        stl = Theme.objects.filter(id=theme_id_)
        styy = stl.values()
        stmp = styy[0]
        context = str(stmp['font_size_header']) + '|' + str(stmp['font_size_menu']) +'|'+ str(stmp['font_size_content_title'])
        return context
    except :
        context = '15'+ '|' + '15' +'|'+ '15'
        return context
    

@register.simple_tag
def appearance_icon_render(icon, enable_shadow=False):
    return icon.render(extra_context={'enable_shadow': enable_shadow})


@register.filter
def appearance_object_list_count(object_list):
    try:
        return object_list.count()
    except TypeError:
        return len(object_list)