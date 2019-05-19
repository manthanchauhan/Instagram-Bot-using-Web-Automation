from InstaBot import InstaBot

if __name__ == "__main__":
    with InstaBot(email='manthanchauhan913@gmail.com',
                  password='YourPasswordHere',
                  username='manthan913') as bot:
        count = bot.inc_followers(host_username='tomcruise',
                                  secon_followers=20,
                                  prim_followers=300,
                                  )
        print(f'followed {count} accounts')

