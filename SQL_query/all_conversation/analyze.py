"""Count conversation 30,000 to 41,000"""

import csv

total_count = 0
mc_count = 0
dont_know_count = 0

with open('./all_conversation.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        row_num = int(row[0])
        if row_num >= 30000 and row_num < 41000:
            total_count += 1
            if "user_quick_reply: NEED_HINT" in row[4]:
                mc_count += 1
            elif "user_quick_reply: I_DONT_KNOW" in row[4]:
                dont_know_count += 1

print('Number of logs: '+ str(total_count))
print('Number of questions in these logs answered by MC: ' + str(mc_count))
print('Number of questions in these logs dont know: ' + str(dont_know_count))
print('Number of questions in these logs answered by typing: ' + str(144))
print('Sum is: ' + str(mc_count+144))
print('A reasonable estimate is: ' + str(int(48*2*40*11000/43956)))

