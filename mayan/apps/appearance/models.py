import bleach

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _

from colorful.fields import RGBColorField

from mayan.apps.databases.model_mixins import ExtraDataModelMixin
from mayan.apps.events.classes import EventManagerSave
from mayan.apps.events.decorators import method_event

from .events import event_theme_created, event_theme_edited

FONT_CHOICES = (
    ('Ubantu','Ubantu font'),
    ('Rubik','Rubik font'),
    ('Inter','Inter font'),
    ('Mukta','Mukta font'),
    ('Kanit','Kanit font'),
    ('Roboto', 'Roboto font'),
    ('Prompt','Prompt font'),
)
class Theme(ExtraDataModelMixin, models.Model):
    label = models.CharField(
        db_index=True,
        max_length=128, unique=True, verbose_name=_('ชื่อธีม')
    )
    stylesheet = models.TextField(
        blank=True,
        verbose_name=_('Stylesheet')
    )
    font = models.CharField(
        max_length=100,
        blank=True,
        choices=FONT_CHOICES,
        verbose_name=_('แบบอักษร')
    )
    color_font_header = RGBColorField(
        blank=True,
        verbose_name=_('สีแบบอักษร')
    )
    background_color_header = RGBColorField(
        blank=True,
        verbose_name=_('สีส่วน Header')
    )
    background_color_menu = RGBColorField(
        blank=True,
        verbose_name=_('สีส่วนพื้นหลัง Menu')
    )
    background_color_header_panel = RGBColorField(
        blank=True,
        verbose_name=_('สีส่วนพื้นหลังเมนูด้านบน')
    )
    background_website = RGBColorField(
        blank=True,
        verbose_name=_('สีพื้นหลังเว็ปไซต์')
    )
    background_menu_dropdown = RGBColorField(
        blank=True,
        verbose_name=_('สีส่วนพื้นหลังเมนูด้านข้าง')
    )
    btn_color_primary = RGBColorField(
        blank=True,
        verbose_name=_('สีปุ่มกด Primary')
    )
    btn_color_danger = RGBColorField(
        blank=True,
        verbose_name=_('สีปุ่มกด Danger')
    )
    btn_color_success = RGBColorField(
        blank=True,
        verbose_name=_('สีปุ่มกด Success')
    )
    btn_color_default = RGBColorField(
        blank=True,
        verbose_name=_('สีปุ่มกด Default')
    )
    font_size_header = models.IntegerField(
        default=19,
        verbose_name=_('ขนาดตัวอักษรส่วน Header')
    )
    font_size_menu = models.IntegerField(
        default=15,
        verbose_name=_('ขนาดตัวอักษรส่วน Menu')
    )
    font_size_content_title = models.IntegerField(
        default=23,
        verbose_name=_('ขนาดตัวอักษรส่วน Content')
    )
    menu_text_color = RGBColorField(
        blank=True,
        verbose_name=_('สีตัวอักษรของเมนูต่างๆ')
    )

    class Meta:
        ordering = ('label',)
        verbose_name = _('Theme')
        verbose_name_plural = _('Themes')

    def __str__(self):
        return force_text(s=self.label)

    def get_absolute_url(self):
        return reverse(
            viewname='appearance:theme_edit', kwargs={
                'theme_id': self.pk
            }
        )

    @method_event(
        event_manager_class=EventManagerSave,
        created={
            'event': event_theme_created,
            'target': 'self',
        },
        edited={
            'event': event_theme_edited,
            'target': 'self',
        }
    )
    def save(self, *args, **kwargs):
        self.stylesheet = bleach.clean(
            text=self.stylesheet, tags=('style',)
        )
        super().save(*args, **kwargs)


class UserThemeSetting(models.Model):
    user = models.OneToOneField(
        on_delete=models.CASCADE, related_name='theme_settings',
        to=settings.AUTH_USER_MODEL, verbose_name=_('User')
    )
    theme = models.ForeignKey(
        blank=True, null=True, on_delete=models.CASCADE,
        related_name='user_setting', to=Theme, verbose_name=_('Theme')
    )

    class Meta:
        verbose_name = _('User theme setting')
        verbose_name_plural = _('User theme settings')

    def __str__(self):
        return force_text(s=self.user)