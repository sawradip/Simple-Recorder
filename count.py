import os, time

folders = [item for item in os.listdir('/storage1/Backup_Kabir/PharmaDataCollection/') if not os.path.isfile(item) and not item == 'venv' and not item == '.git']

print('*'*75 + '\n')
while True:
    for folder in folders:
        print(f'"{folder}" has generated {len(os.listdir(folder))} data. \n')
    print('*'*75 + '\n')
    time.sleep(5)