from datetime import datetime
from dateutil.relativedelta import relativedelta

async def math_day_for_db(data):
    if len(data) == 2:
        day = data['day']
        month = int(data['month'].split('_')[1])

        if month < 10:
            month = "0" + str(month)
        else:
            month = str(month)
        date = day + "." + month
        return await math_date(date)

    else:
        days = data['days'].split('d')[0]
        return await math_date(days)



async def math_date(date):
    if '.' in date:
        dtn = datetime.now()
        YEAR = int(dtn.strftime("%Y"))
        dt = dtn.strptime(date, "%d.%m").replace(YEAR).date()
        print(dt)
        return dt
    else:
        date = int(date)
        end_trial = (datetime.now() + relativedelta(days=date)).date()
        print(end_trial)
        return end_trial
