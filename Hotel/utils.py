from hashlib import sha512
import string, random


def generate_random_os_booking_id():
    os_booking_id = 'OSH' + str(random.randint(100000000, 9999999999))
    return os_booking_id

def encrypt_pay(pay_hash):
    size = 32
    res = bytes(pay_hash, 'utf-8')
    hashed = sha512(res).hexdigest()
    return hashed