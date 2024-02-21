import random

class _random_creator:
    def acc(unme:str):
        try:
            username=unme

            rn=random.random()


        except Exception as e:
            print(f'_RANDOM_CREATOR ERRROR: [{str(e)}]')

print(random.randint(1000,10))
