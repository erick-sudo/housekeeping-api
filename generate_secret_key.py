import os
from django.core.management.utils import get_random_secret_key

# Write the secret key to a .env file
with open('.env', 'a') as f:
    f.write(f'\nSECRET_KEY={get_random_secret_key()}{get_random_secret_key()}\n')

print('Secret key generated and saved to .env file.')