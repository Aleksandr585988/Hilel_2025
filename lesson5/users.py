
users = {
    'admin': 'admin',
}

cache = {}


def auth(func):
    def wrapper(*args, **kwargs):
        if 'username' in cache and 'password' in cache:
            print("Authorization completed using cache.")

            return func(*args, **kwargs)

        while True:
            username = input("Enter your name: ")
            password = input("Enter password: ")

            if username in users and users[username] == password:
                print("Authorization successful!")
                cache['username'] = username
                cache['password'] = password
                return func(*args, **kwargs)
            else:
                print("Incorrect data. Please try again.")
    return wrapper


@auth
def command():
    print("Command executed!")


command()
command()
