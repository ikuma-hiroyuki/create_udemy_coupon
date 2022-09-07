import random
import string

codes_file = "codes.txt"


def random_name(n: int):
    letters = string.ascii_uppercase + string.digits + '.' + '_' + '-'
    return ''.join(random.choices(letters, k=n))


for _ in range(10):
    with open(codes_file, "r") as read_file:
        past_codes = [code.replace("\n", "") for code in read_file.readlines()]

    code = random_name(10)

    while code in past_codes:
        code = random_name(10)

    with open(codes_file, "a") as write_file:
        write_file.writelines(f"{code}\n")
        print(code)
