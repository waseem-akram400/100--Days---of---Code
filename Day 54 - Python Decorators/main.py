def my_decorator(function):
    def wrapper():
        print("فنکشن شروع ہونے والا ہے")
        function()
        print("فنکشن مکمل ہو گیا")
    return wrapper


@my_decorator
def say_hello():
    print("Assalam-o-Alaikum!")


say_hello()