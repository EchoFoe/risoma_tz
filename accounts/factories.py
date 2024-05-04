from faker import Faker
from .models import Account

fake = Faker()


class UserFactory:
    @staticmethod
    def create_fake_user() -> Account:
        """Создает фантомного пользователя."""
        first_name: str = fake.first_name()
        last_name: str = fake.last_name()
        username: str = f"{first_name.lower()}.{last_name.lower()}"
        password: str = 'password'
        phone: str = fake.phone_number()[:15]
        return Account.objects.create_user(
            username=username, password=password, first_name=first_name, last_name=last_name, phone=phone
        )
