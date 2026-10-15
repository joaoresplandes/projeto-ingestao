from Pipeline.Bronze.executar import RotinaBronze
from Pipeline.Silver.executar import RotinaSilver
from Pipeline.Gold.executar import RotinaGold
from time import sleep
import schedule


def rotina_principal():
    RotinaBronze().executar()
    RotinaSilver().executar()
    RotinaGold().executar()


if __name__ == '__main__':

    schedule.every().day().at('02:00').do(rotina_principal)
    while True:
        schedule.run_pending()
        sleep(1)
