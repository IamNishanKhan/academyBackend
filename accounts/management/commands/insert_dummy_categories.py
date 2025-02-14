from django.core.management.base import BaseCommand
from courses.models import Category  # Adjust if your model is in a different app

class Command(BaseCommand):
    help = 'Create dummy categories for engineering courses'

    def handle(self, *args, **kwargs):
        categories = [
            'Computer Science',
            'Electrical Engineering',
            'Mechanical Engineering',
            'Civil Engineering',
            'Chemical Engineering',
            'Aerospace Engineering',
            'Environmental Engineering',
            'Biotechnology Engineering',
            'Industrial Engineering',
            'Software Engineering',
        ]

        for category_name in categories:
            Category.objects.create(category_name=category_name)

        self.stdout.write(self.style.SUCCESS('Successfully created 10 engineering categories'))
