import datetime

initialDate = datetime.datetime.strptime("2016-02-08 05:46:00", '%Y-%m-%d %H:%M:%S')
print(initialDate.time().minute)


