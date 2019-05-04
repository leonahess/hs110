from pyHS100 import Discover
from threading import Thread
from app.hs110 import HS110


def main():

    threads = []

    for dev in Discover.discover():
        threads.append(Thread(name=dev, target=HS110, args=(dev,)))

    for thread in threads:
        thread.start()
        print("< {}".format(thread))


if __name__ == "__main__":
    main()
