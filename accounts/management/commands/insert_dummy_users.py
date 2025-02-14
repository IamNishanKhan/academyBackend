from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string
from accounts.models import User  # Replace with your app's name if it's different

class Command(BaseCommand):
    help = 'Insert 20 dummy users (5 instructors, 15 students)'

    def handle(self, *args, **kwargs):
        # Instructors
        instructor1 = User.objects.create_user(
            first_name='John',
            last_name='Doe',
            email='john.doe1@example.com',
            phone='1234567890',
            password=get_random_string(12),
            role='instructor',
        )
        self.stdout.write(f'Instructor created: {instructor1.email}')

        instructor2 = User.objects.create_user(
            first_name='Jane',
            last_name='Smith',
            email='jane.smith2@example.com',
            phone='1234567891',
            password=get_random_string(12),
            role='instructor',
        )
        self.stdout.write(f'Instructor created: {instructor2.email}')

        instructor3 = User.objects.create_user(
            first_name='Michael',
            last_name='Johnson',
            email='michael.johnson3@example.com',
            phone='1234567892',
            password=get_random_string(12),
            role='instructor',
        )
        self.stdout.write(f'Instructor created: {instructor3.email}')

        instructor4 = User.objects.create_user(
            first_name='Emily',
            last_name='Davis',
            email='emily.davis4@example.com',
            phone='1234567893',
            password=get_random_string(12),
            role='instructor',
        )
        self.stdout.write(f'Instructor created: {instructor4.email}')

        instructor5 = User.objects.create_user(
            first_name='David',
            last_name='Martinez',
            email='david.martinez5@example.com',
            phone='1234567894',
            password=get_random_string(12),
            role='instructor',
        )
        self.stdout.write(f'Instructor created: {instructor5.email}')

        # Students
        student1 = User.objects.create_user(
            first_name='Sophia',
            last_name='Brown',
            email='sophia.brown1@example.com',
            phone='1234567895',
            password=get_random_string(12),
            role='student',
        )
        self.stdout.write(f'Student created: {student1.email}')

        student2 = User.objects.create_user(
            first_name='James',
            last_name='Wilson',
            email='james.wilson2@example.com',
            phone='1234567896',
            password=get_random_string(12),
            role='student',
        )
        self.stdout.write(f'Student created: {student2.email}')

        student3 = User.objects.create_user(
            first_name='Olivia',
            last_name='Moore',
            email='olivia.moore3@example.com',
            phone='1234567897',
            password=get_random_string(12),
            role='student',
        )
        self.stdout.write(f'Student created: {student3.email}')

        student4 = User.objects.create_user(
            first_name='Liam',
            last_name='Taylor',
            email='liam.taylor4@example.com',
            phone='1234567898',
            password=get_random_string(12),
            role='student',
        )
        self.stdout.write(f'Student created: {student4.email}')

        student5 = User.objects.create_user(
            first_name='Isabella',
            last_name='Anderson',
            email='isabella.anderson5@example.com',
            phone='1234567899',
            password=get_random_string(12),
            role='student',
        )
        self.stdout.write(f'Student created: {student5.email}')

        student6 = User.objects.create_user(
            first_name='Mason',
            last_name='Thomas',
            email='mason.thomas6@example.com',
            phone='1234567800',
            password=get_random_string(12),
            role='student',
        )
        self.stdout.write(f'Student created: {student6.email}')

        student7 = User.objects.create_user(
            first_name='Charlotte',
            last_name='Jackson',
            email='charlotte.jackson7@example.com',
            phone='1234567801',
            password=get_random_string(12),
            role='student',
        )
        self.stdout.write(f'Student created: {student7.email}')

        student8 = User.objects.create_user(
            first_name='Elijah',
            last_name='White',
            email='elijah.white8@example.com',
            phone='1234567802',
            password=get_random_string(12),
            role='student',
        )
        self.stdout.write(f'Student created: {student8.email}')

        student9 = User.objects.create_user(
            first_name='Amelia',
            last_name='Harris',
            email='amelia.harris9@example.com',
            phone='1234567803',
            password=get_random_string(12),
            role='student',
        )
        self.stdout.write(f'Student created: {student9.email}')

        student10 = User.objects.create_user(
            first_name='Benjamin',
            last_name='Martin',
            email='benjamin.martin10@example.com',
            phone='1234567804',
            password=get_random_string(12),
            role='student',
        )
        self.stdout.write(f'Student created: {student10.email}')

        student11 = User.objects.create_user(
            first_name='Amos',
            last_name='Lee',
            email='amos.lee11@example.com',
            phone='1234567805',
            password=get_random_string(12),
            role='student',
        )
        self.stdout.write(f'Student created: {student11.email}')

        student12 = User.objects.create_user(
            first_name='Chloe',
            last_name='Gonzalez',
            email='chloe.gonzalez12@example.com',
            phone='1234567806',
            password=get_random_string(12),
            role='student',
        )
        self.stdout.write(f'Student created: {student12.email}')

        student13 = User.objects.create_user(
            first_name='Jacob',
            last_name='Perez',
            email='jacob.perez13@example.com',
            phone='1234567807',
            password=get_random_string(12),
            role='student',
        )
        self.stdout.write(f'Student created: {student13.email}')

        student14 = User.objects.create_user(
            first_name='Ava',
            last_name='Wilson',
            email='ava.wilson14@example.com',
            phone='1234567808',
            password=get_random_string(12),
            role='student',
        )
        self.stdout.write(f'Student created: {student14.email}')

        student15 = User.objects.create_user(
            first_name='Lucas',
            last_name='Young',
            email='lucas.young15@example.com',
            phone='1234567809',
            password=get_random_string(12),
            role='student',
        )
        self.stdout.write(f'Student created: {student15.email}')

        self.stdout.write(self.style.SUCCESS('Successfully created 20 dummy users.'))
