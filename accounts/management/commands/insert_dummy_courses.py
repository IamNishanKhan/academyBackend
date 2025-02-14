from django.core.management.base import BaseCommand
from accounts.models import User
from courses.models import Course
from categories.models import Category

class Command(BaseCommand):
    help = 'Insert dummy courses'

    def handle(self, *args, **kwargs):
        # Fetch instructors by role
        instructors = User.objects.filter(role='instructor')

        if instructors.count() < 5:
            self.stdout.write(self.style.ERROR('Not enough instructors. Please make sure there are at least 5 instructors.'))
            return

        categories = Category.objects.all()

        if categories.count() == 0:
            self.stdout.write(self.style.ERROR('No categories found. Please make sure there are categories in the database.'))
            return

        # Define the courses for each instructor
        courses_data = [
            {"title": "Introduction to AI", "description": "AI basics", "price": 199.99, "category": categories[0]},
            {"title": "Advanced Python Programming", "description": "Deep dive into Python", "price": 249.99, "category": categories[1]},
            {"title": "Web Development with Django", "description": "Learn Django framework", "price": 299.99, "category": categories[2]},
            {"title": "Data Science Fundamentals", "description": "Introduction to Data Science", "price": 279.99, "category": categories[3]},
            {"title": "Machine Learning Basics", "description": "Fundamentals of ML", "price": 259.99, "category": categories[4]},
            {"title": "Cloud Computing Essentials", "description": "Basics of Cloud Computing", "price": 229.99, "category": categories[5]},
            {"title": "JavaScript for Beginners", "description": "Learn JavaScript from scratch", "price": 199.99, "category": categories[6]},
            {"title": "Database Management Systems", "description": "Learn DBMS fundamentals", "price": 249.99, "category": categories[7]},
            {"title": "Cybersecurity Fundamentals", "description": "Introduction to Cybersecurity", "price": 269.99, "category": categories[8]},
            {"title": "Introduction to Networking", "description": "Network fundamentals", "price": 219.99, "category": categories[9]},
        ]

        # Assign 2 courses per instructor
        for i, instructor in enumerate(instructors[:5]):  # Only pick the first 5 instructors
            for j in range(2):  # Assign 2 courses to each instructor
                course_data = courses_data[i * 2 + j]  # Select 2 courses for the instructor
                course = Course.objects.create(
                    title=course_data['title'],
                    description=course_data['description'],
                    price=course_data['price'],
                    category=course_data['category'],
                    user=instructor  # Assign the instructor as the user
                )
                self.stdout.write(self.style.SUCCESS(f'Course created: {course.title} by {instructor.first_name} {instructor.last_name}'))
