import os, time

folders = [item for item in os.listdir('/storage1/Backup_Kabir/PharmaDataCollection/') if not os.path.isfile(item) and not item == 'venv' and not item == '.git']

print('*'*75 + '\n')
while True:
    sum = 0
    for folder in folders:
        print(f'"{folder}" has generated {len(os.listdir(folder))} data. \n')
        sum += len(os.listdir(folder))
    print(f"Total number of files: {sum} \n")
    print('*'*75 + '\n')
    time.sleep(5)