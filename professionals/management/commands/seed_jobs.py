<<<<<<< HEAD
from django.core.management.base import BaseCommand
from professionals.models import Job

class Command(BaseCommand):
    help = 'وارد کردن مشاغل اولیه'

    def handle(self, *args, **kwargs):
        jobs = [
            ('stylist', 'آرایشگر'),
            ('developer', 'برنامه‌نویس'),
            ('doctor', 'پزشک'),
            ('coach', 'مربی ورزشی'),
            ('mechanic', 'مکانیک'),
            ('lawyer', 'وکیل'),
            ('designer', 'طراح'),
            ('electrician', 'برق‌کار'),
            ('plumber', 'لوله‌کش'),
            ('psychologist', 'روانشناس'),
        ]


        for code, title in jobs:
            obj, created = Job.objects.get_or_create(code=code, defaults={'title': title})
            if created:
                self.stdout.write(self.style.SUCCESS(f"{title} اضافه شد."))
            else:
                self.stdout.write(f"{title} قبلاً وجود داشته.")
=======
from django.core.management.base import BaseCommand
from professionals.models import Job

class Command(BaseCommand):
    help = 'وارد کردن مشاغل اولیه'

    def handle(self, *args, **kwargs):
        jobs = [
            ('stylist', 'آرایشگر'),
            ('developer', 'برنامه‌نویس'),
            ('doctor', 'پزشک'),
            ('coach', 'مربی ورزشی'),
            ('mechanic', 'مکانیک'),
            ('lawyer', 'وکیل'),
            ('designer', 'طراح'),
            ('electrician', 'برق‌کار'),
            ('plumber', 'لوله‌کش'),
            ('psychologist', 'روانشناس'),
        ]


        for code, title in jobs:
            obj, created = Job.objects.get_or_create(code=code, defaults={'title': title})
            if created:
                self.stdout.write(self.style.SUCCESS(f"{title} اضافه شد."))
            else:
                self.stdout.write(f"{title} قبلاً وجود داشته.")
>>>>>>> 100bba5 (Inititial commit)
