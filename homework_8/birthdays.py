"""
функцию для вывода списка коллег, которых надо
поздравить с днём рождения на неделе.
"""

from datetime import datetime, timedelta

people = [
    {'name': 'Vitalii Kuchma', 'birthday': '20.06.2001'},
    {'name': 'Olesia', 'birthday': '13.06.2002'},
    {'name': 'Irina', 'birthday': '19.06.2003'},
    {'name': 'Sasha', 'birthday': '15.06.2008'},
    {'name': 'Andryi', 'birthday': '26.06.2004'},
    {'name': 'Pasha Poplov', 'birthday': '27.06.1997'},
    {'name': 'Gaga Ledi', 'birthday': '18.06.1998'},
    {'name': 'Oksana Rembo', 'birthday': '11.06.2005'}
]


def get_birthdays_per_week(users: list):
    mon = []
    tues = []
    wed = []
    thurs = []
    fri = []

    result = {
        'Monday': mon,
        'Tuesday': tues,
        'Wednesday': wed,
        'Thursday': thurs,
        'Friday': fri
    }

    today = datetime.now()
    week_now = today.strftime('%W')
    year_ = today.year

    for person in users:
        birthday = person.get('birthday')
        m_b = datetime.strptime(birthday, '%d.%m.%Y')
        m_b = m_b.replace(year=year_)
        day = m_b.strftime('%w')
        if day == '0':
            m_b = m_b + timedelta(days=1)
        if day == '6':
            m_b = m_b + timedelta(days=2)
        week = m_b.strftime('%W')

        if week == week_now:
            if day == '1' or day == '6' or day == '0':
                mon.append(person.get('name'))

            elif day == '2':
                tues.append(person.get('name'))

            elif day == '3':
                wed.append(person.get('name'))

            elif day == '4':
                thurs.append(person.get('name'))

            elif day == '5':
                fri.append(person.get('name'))

    for k, v in result.items():
        return f'{k}: {", ".join(v)}'


print(get_birthdays_per_week(people))
print('Happy birthday, dears!!!')
