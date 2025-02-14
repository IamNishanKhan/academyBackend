from django.core.management.base import BaseCommand
from modules.models import Module
from lessons.models import Lesson  # Assuming your Lesson model is in the lessons app

class Command(BaseCommand):
    help = 'Create 3 lessons for each module'

    def handle(self, *args, **kwargs):
        modules = Module.objects.all()  # Get all modules

        if modules.count() == 0:
            self.stdout.write(self.style.ERROR('No modules found. Please ensure there are modules to associate lessons with.'))
            return

        lesson_count = 1  # Start numbering lessons
        for module in modules:
            for i in range(1, 4):  # Create 3 lessons for each module
                lesson_title = f"Lesson {i}"
                video_url = f"http://example.com/video_{lesson_count}.mp4"  # Dummy URL
                duration = 300  # Dummy duration (5 minutes)
                Lesson.objects.create(
                    module=module,
                    title=lesson_title,
                    video_url=video_url,
                    duration=duration,
                    order=i
                )
                lesson_count += 1

        self.stdout.write(self.style.SUCCESS('Successfully created 3 lessons for each module.'))
