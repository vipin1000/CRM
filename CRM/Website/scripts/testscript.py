# Test in Django shell
from Website.models import Record

# This should raise a ValidationError
def run():
    record = Record(
        first_name="John",  # Does not start with "M"
        last_name="Doe",
        email="john.doe@example.com",
        phone="1234567890",
        address="123 Main St",
        city="New York",
        state="NY",
        Pincode="123456"
    )
    record.full_clean()