from django.db import models
from django.urls import reverse
from django.core.files import File
from io import BytesIO
from PIL import Image, ImageDraw
import qrcode


class Animals(models.Model):
    animal_name = models.CharField(max_length=100, help_text='Ievadiet dzīvnieka nosaukumu', verbose_name='Nosaukums')
    family_name = models.ForeignKey('Family', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Dzimta',
                                    help_text='Izvēlieties dzīvnieka dzimtu')
    latin_name = models.CharField(max_length=100, help_text='Ievadiet dzīvnieka pilno latīņu nosaukumu',
                                  verbose_name='Latīņu nosaukums')
    text = models.TextField(help_text='Ievadiet tekstuālu aprakstu par dzīvnieku', verbose_name='Teksts')
    image = models.ImageField(upload_to='photos/%Y/%m/%d/', help_text='Augšupielādējiet attēlu ar dzīvnieku',
                              verbose_name='Bilde')
    qr_code = models.ImageField(upload_to='photos/qr_codes', blank=True, null=True, verbose_name='QR-kods')
    prefix = models.URLField(help_text='Ievadiet domēna nosaukumu, kā prefiksu priekš QR-koda saites',
                             verbose_name='Domēns',
                             default='http://192.168.1.64:8000')

    def save(self, *args, **kwargs):
        qrcode_img = qrcode.make(self.prefix)
        super().save(*args, **kwargs)
        if qrcode_img:
            qrcode_img = qrcode.make(self.prefix + self.get_absolute_url())
            canvas = Image.new('RGB', (qrcode_img.pixel_size, qrcode_img.pixel_size), 'white')
            draw = ImageDraw.Draw(canvas)
            canvas.paste(qrcode_img)
            fname = f'qr_code-{self.get_absolute_url()}'+'.png'
            buffer = BytesIO()
            canvas.save(buffer, 'PNG')
            self.qr_code.save(fname, File(buffer), save=False)
            canvas.close()
            super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('view_animals', kwargs={"pk": self.pk})

    def __str__(self):
        return self.animal_name

    class Meta:
        verbose_name = 'Dzīvnieks'
        verbose_name_plural = 'Dzīvnieki'
        ordering = ['-id']


class Family(models.Model):
    name = models.CharField(max_length=35, help_text='Ievadiet dzīvnieka dzimtu (ģenitīva locījumā, daudzskaitlī)',
                            verbose_name='Dzimta', db_index=True)

    def get_absolute_url(self):
        return reverse('family', kwargs={"family_id": self.pk})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Dzimta'
        verbose_name_plural = 'Dzimtas'
        ordering = ['-id']
