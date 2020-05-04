from datetime import datetime
import time


def cannot_use(func):
    def wrapper(*args, **kwargs):
        raise NotImplementedError
    return wrapper


def moodle_deadline_strategy(webmaster, delay, range):
    deadlines = webmaster.query('Moodle', 'scrapeDeadlines')
    if len(deadlines) > 0:
        near_deadline = deadlines[0]
        return [{
            'type': 'relative',
            'range': range,
            'delay': delay,
            'msg': '<a href="{}">{}: {}</a>'.format(near_deadline['link'], near_deadline['name'], near_deadline['time'])
        }]
    else:
        return []


def simple_alarm_strategy(webmaster, delay, range):
    return [{
        'type': 'relative',
        'range': range,
        'delay': delay,
        'msg': 'this is an alarm'
    }]


def portal_next_lesson_strategy(webmaster, delay, range):
    timetable = webmaster.query('Portal', 'findWeeklySch', datetime.now().strftime('%d/%m/%y'), '8:00AM', '11:00PM')
    result = []
    for time_slot in timetable:
        start_time = time_slot['time'].split(' - ')[0]
        datetime_object = datetime.strptime(time_slot['date'] + ' ' + str(datetime.now().year) + ' ' + start_time, '%d %b %Y %I:%M%p')
        if datetime_object.day == datetime.today().day and datetime.today().hour < datetime_object.hour:
            due_time = time.mktime(datetime_object.timetuple()) + datetime_object.microsecond / 1E6
            result.append({
                'type': 'absolute',
                'range': range,
                'time': due_time,
                'msg': '{} is coming on {}:{}'.format(time_slot['course'], datetime_object.hour, datetime_object.minute)
            })
    return result


def portal_get_invoice_strategy(webmaster, delay, range):
    invoice_info = webmaster.query('Portal', 'findInvoice')
    # for key in invoice_info.keys():
    #     print(key)
    #     for row in invoice_info[key]:
    #         print(row)
    total_due = invoice_info['TOTAL_DUE']
    if total_due[1][0] == '' and total_due[1][1] == '' and total_due[1][2] == '':
        return []
    else:
        return [{
            'type': 'relative',
            'range': range,
            'delay': delay,
            'msg': '${} is due on {}'.format(total_due[1][1], total_due[1][0])
        }]


@cannot_use
def moodle_course_updated(webmaster, delay, range):
    transcript_info = webmaster.query('Portal', 'findTranscript')
    # for row in transcript_info['CRSE_HIST']:
    #     print(row)
    if datetime.now().month < 9:
        semester = str(datetime.now().year - 1) + '-' + str(datetime.now().year % 100) + ' Sem ' + str(2)
    else:
        semester = str(datetime.now().year) + '-' + str( (datetime.now().year + 1) % 100) + ' Sem ' + str(1)
    # print(semester)
    course_list = []
    for row in transcript_info['CRSE_HIST']:
        if row[2] == semester:
            course_list.append(row[0][:4] + row[0][5:])
    # print(course_list)
    for course in course_list:
        try:
            result = webmaster.query('Moodle', 'findCourseByKeywords', course)
            # print(result)
        except:
            pass

    return []
