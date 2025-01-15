import os
from dotenv import load_dotenv
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute
from pynamodb.exceptions import DoesNotExist

class UserModel(Model):
    class Meta:
        table_name = "users"
        region = "ap-southeast-1"
        aws_access_key_id = os.getenv('AWS_ACCESS_KEY')
        aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

    email = UnicodeAttribute(hash_key=True, null=False)
    password = UnicodeAttribute()


# Create the table if it doesn't exist
