from django.core.management.base import BaseCommand
from courses.models import Course
from modules.models import Module  # Assuming your Module model is in the modules app

class Command(BaseCommand):
    help = 'Create 5 modules for each course'

    def handle(self, *args, **kwargs):
        courses = Course.objects.all()  # Get all courses

        if courses.count() == 0:
            self.stdout.write(self.style.ERROR('No courses found. Please ensure there are courses to associate modules with.'))
            return

        for course in courses:
            for i in range(1, 6):  # Create 5 modules for each course
                module_title = f"Module {i}"
                Module.objects.create(
                    course=course,
                    title=module_title,
                    order=i
                )

        self.stdout.write(self.style.SUCCESS('Successfully created 5 modules for each course.'))
