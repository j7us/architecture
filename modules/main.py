from cleaner import Cleaner
import transfers

code = (
    'move 100',
    'turn -90',
    'set soap',
    'start',
    'move 50',
    'stop'
)

def main():
    cleaner = Cleaner(transfers.transfer_to_cleaner)
    cleaner.execute(code)

main()
