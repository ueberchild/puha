# import os
# os.system('pip3 install -r requirements.txt')
# import platform
# if platform.system() == 'Windows': os.system('doc_to_docx.bat')
# else: os.system('bash doc_to_docx.sh')

import pandas as pd, re, openpyxl, io, csv, calendar, docx, datetime

YEAR = 2020

class curric:
    def __init__(self, program_type, time_borders, personnel_type, specialization):
        self.program_type = program_type
        self.personnel_type = personnel_type
        self.specialization = specialization
        self.days = []
        
        day, month = time_borders[0].split('.')
        sdate = datetime.date(YEAR, month, day)
        day, month = time_borders[1].split('.')
        edate = datetime.date(YEAR, month, day)
        delta = edate - sdate
        for i in range(delta.days + 1):
            self.days.append(sdate + datetime.timedelta(days = i))
    
    def __eq__(self, other):
        return self.program_type == other.program_type and \
               self.time_borders == other.time_borders and \
               self.personnel_type == other.personnel_type and \
               self.specialization == other.specialization
    
    def pick_lecturers_and_auditories(self):
        self.lecturers = []
        self.auditories = []
        for _, pair in self.calendar.iterrows():
            pair_lecturers = []
            pair_auditories = []
            theory_pair = False
            practice_pair = False
            for t in pair['Тема'].split('\n'):
                if self.plan[self.plan['Наименование разделов и тем'] == t].iloc[0, 3] != '–':
                    theory_pair = True
                if self.plan[self.plan['Наименование разделов и тем'] == t].iloc[0, 4] != '–':
                    practice_pair = True
            pair_day = self.days[0] + datetime.timedelta(days = pair['День'] - 1)
            
            lecturer_candidates = []
            for _, l in lecturers_pars.iterrows():
                if not str(self.theme[1]) in l['Учебные программы'].split(';'):
                    continue
                if not lecturer_is_free(l['Преподаватель'], pair_day, pair['Время']):
                    continue
                terror_theme = False
                if self.theme[1] == 34 and re.search('Тема 4', pair['Тема']) or self.theme[1] == 35 and re.search('Тема 8', pair['Тема']):
                    terror_theme = True   
                if 'за исключением тем с 4 раздела в программе 34 и  тем с раздела 8 в программе 35' in l['Может проводить занятия по темам']\
                    and terror_theme: continue
                if 'только разделы с 4 по программе 34, разделы с 8 на программе 35' in l['Может проводить занятия по темам']\
                    and not terror_theme: continue
                if self.theme[1] == 31 and 'темы № 8.7  в программе 31,а так же раздела 5' in l['Может проводить занятия по темам']\
                    and (re.search('Тема 8.7', pair['Тема']) or re.search('Тема 5', pair['Тема'])): continue
                l_priority = l['Приоритет при распределении']
                if not l_priority or l_priority in ('нет', 'в рабочие смены', 'необходим выходной после каждого второго рабочего дня'):
                    l_priority = 1.5
                elif l_priority == 'при распределении на программы 7 и 8 - приоритет 1' and self.theme[1] in (7, 8) or\
                     l_priority == 'при распределении на программы 11 и 12- приоритет 1' and self.theme[1] in (11, 12):
                    l_priority = 1
                elif l_priority == '1 - на теоретические занятия, 2 - на практические':
                    if theory_pair: l_priority = 1
                    else l_priority = 2
                elif l_priority == '1- на практические занятия, 2 на теоретические':
                    if practice_pair: l_priority = 1
                    else l_priority = 2
                elif l_priority == 'если нет других свободных преподавателей':
                    l_priority = 4
                else:
                    l_priority = int(l_priority)
                lecturer_candidates.append((l['Преподаватель'], l_priority))
            
            lecturer_candidates.sort(key = lambda x: x[1])
            chosen_lecturer = lecturer_candidates[0][0]
            if not pair_day in lecturer_busy[chosen_lecturer]:
                lecturer_busy[chosen_lecturer][pair_day] = []
            lecturer_busy[chosen_lecturer][pair_day].append(pair['Время'])
            pair_lecturers.append(chosen_lecturer)
            self.lecturers.append(pair_lecturers)
            
            auditory_candidates = []
            for _, a in auditory_pars.iterrows():
                if pair_day in auditory_busy[name] and time in auditory_busy[l][day]:
                if theory_pair and not 'теоретические' in a['Вид занятий'] or \
                 practice_pair and not 'практические'  in a['Вид занятий']:
                    continue
                if a['Подходит для дисциплин'] == 'кроме Подготовка преподавателей АУЦ' and self.theme[1] in (5, 6):
                    continue
                if a['Подходит для дисциплин'] == 'Авиационная безопасность, \nтолько для практических занятий по программам №30, 31 и 32' \
                    and not (practice_pair and self.theme[1] in (30, 31, 32)):
                    continue
                if self.theme[0] == 'Аварийно-спасательное обеспечение полетов' and\
                     a['Подходит для дисциплин'] != 'Аварийно-спасательное обеспечение полетов':
                    continue
                if self.theme[0] != 'Аварийно-спасательное обеспечение полетов' and\
                     a['Подходит для дисциплин'] == 'Аварийно-спасательное обеспечение полетов':
                    continue
                if a['Подходит для дисциплин'] == 'Организация наземного обслуживания;\nЦентровка и контроль загрузки' and\
                     not self.theme[1] in (1, 2, 15, 16)
                     continue
                if a['Подходит для дисциплин'] == 'Водители; ПОЗ ВС' and not 17 <= self.theme[1] <= 29:
                    continue
                a_priority = 2
                if a['Преимущество у дисциплины'] == 'Авиационная безопасность' and 30 <= self.theme[1] <= 39 or\
                   a['Преимущество у дисциплины'] == 'Центровка и контроль загрузки' and self.theme[1] in (1, 2) or\
                   a['Преимущество у дисциплины'] == 'Организация наземного обслуживания' and self.theme[1] in (15, 16) or\
                   a['Преимущество у дисциплины'] == 'Водители' and 22 <= self.theme[1] <= 29:
                    a_priority = 1
                auditory_candidates.append(a['Аудитория'], a_priority)
            
            auditory_candidates.sort(key = lambda x: x[1])
            chosen_auditory = auditory_candidates[0][0]
            if not pair_day in auditory_busy[chosen_lecturer]:
                auditory_busy[chosen_auditory][pair_day] = []
            auditory_busy[chosen_auditory][pair_day].append(pair['Время'])
            pair_auditories.append(chosen_auditory)
            self.auditories.append(pair_auditories)

'''
class lecturer:
    def __init__():
        self.theory_only = False
        self.practice_preferred = False
        self.
'''

def lecturer_is_free(name, datet, time):
    #lecturer_row = vacation_schedule.index[vacation_schedule.iloc[:,1] == name].tolist()[0]
    if datet in lecturer_busy[name] and time in lecturer_busy[name][datet]:
        return False
    
    if name == 'Некрасова Л.Д.' and \
       datet - datetime.timedelta(days = 1) in lecturer_busy[name] and \
       datet - datetime.timedelta(days = 2) in lecturer_busy[name]:
        return False
    
    if lecturers_pars.loc[name, 'График работы'] == 'сменный':
        shifts = re.findall('\d', lecturers_pars.loc[name, 'График сменности'])
        for shift in shifts:
            shift_row = 3 + 7 * months
            if shift == '3':
                shift_row += 1
            elif shift == '4':
                shift_row += 2
            elif shift == '1':
                shift_row += 3
            if shift_schedule.iloc[shift_row, datet.day] != 'д':
                return False
    elif lecturers_pars.loc[name, 'График работы'] == 'пятидневный' and \
         datetime.date(YEAR, datet.month, datet.day).weekday() >= 5:
        return False
    
    for m in range(12):
        vacation_days = vacation_schedule.iloc[:, 3 + 2 * m]
        vacation_decade = vacation_schedule.iloc[:, 4 + 2 * m]
        if type(vacation_days) == int:
            if m == datet.month and vacation_decade * 10 < datet.day < vacation_decade * 10 + vacation_days:
                return False
            for next_month in range(m + 1, 12):
                if next_month == m + 1:
                    vacation_days -= calendar.monthrange(YEAR, m)[1] - vacation_decade
                else:
                    vacation_days -= calendar.monthrange(YEAR, next_month - 1)[1]
                if vacation_days <= 0: break
                if datet.month == next_month and datet.day <= vacation_days:
                    return False
    
    return True

def read_docx_tables(filename, tab_id=None, **kwargs):
    def read_docx_tab(tab, **kwargs):
        vf = io.StringIO()
        writer = csv.writer(vf)
        for row in tab.rows:
            writer.writerow(cell.text for cell in row.cells)
        vf.seek(0)
        return pd.read_csv(vf, **kwargs)
    
    return [read_docx_tab(tab, **kwargs) for tab in docx.Document(filename).tables]

'''
def read_excel_without_invis(fname): 
    wb = openpyxl.load_workbook(fname)
    ws = wb.worksheets[0]
    hidden_cols = set()
    for col_letter, col_dimensions in ws.column_dimensions.items():
        if col_dimensions.hidden == True:
            hidden_cols.add(col_letter)
    return pd.read_excel(fname).drop(list(hidden_cols), axis = 1)
'''

a_1 = pd.read_excel('data/Приложение №1.xlsx').dropna(how='all').dropna(how='all',axis=1)
a_1.drop(a_1.columns[0:2], axis = 1, inplace = True)
curriculum_pars = pd.read_excel('data/Приложение №2.xlsx', sheet_name = 0)
auditory_pars = pd.read_excel('data/Приложение №2.xlsx', sheet_name = 1).rename(columns={'Аудитрия':'Аудитория'}).set_index('Аудитория')
lecturers_pars = pd.read_excel('data/Приложение №2.xlsx', sheet_name = 2).set_index('Преподаватель')
shift_schedule = pd.read_excel('data/Приложение №4.xlsx')
vacation_schedule = pd.read_excel('data/Приложение №5.xls')

currics = []

for (month, col_d) in a_1.iteritems():
    if col_d.any() and 'Неделя' in str(col_d.iloc[0]):
        for plan_num, week_plan in enumerate(col_d):
            if type(week_plan) == str and week_plan:
                week_currics = week_plan.split('\n\n')
                for w_l in week_currics:
                    w_l_info = w_l.split('\n')
                    if len(w_l_info) == 3 and type(a_1.iloc[plan_num, 0]) == str:
                        time_borders = re.findall('\d*\.\d*', w_l_info[1].replace('..', '.'))
                        personnel_type = 'av' if plan_num < 6 else 'notav'
                        # if ' ' in w_l_info[2]:
                        #     auditory = w_l_info[2].split(' ')[-1]
                        # elif '.' in w_l_info[2]:
                        #     auditory = w_l_info[2].split('.')[-1]
                        currics.append(curric(w_l_info[0], time_borders, personnel_type, a_1.iloc[plan_num, 0]))

currics = list(dict.fromkeys(currics)) # rm duplicates

for c in tuple(curriculum_pars.columns):
    for row in range(len(curriculum_pars)):
        if type(curriculum_pars.at[row, c]) == int:
            curriculum_pars.at[row, c] = max(0, curriculum_pars.at[row, c])
  
lecturers_busy = {}
for l in lecturers_pars['Преподаватель']:
    lecturers_busy[l] = {}

auditories_busy = {}
for a in auditory_pars['Аудитория']:
    auditories_busy[a] = {}

curriculum_pars['Учебная программа'] = curriculum_pars['Учебная программа'].apply(lambda x: re.sub(r'(?<=[.,])(?=[^\s])', r' ', x.strip().replace('«', '"').replace('»', '"')))

disciplines_dict = {
    'Досмотр': (('Авиационная безопасность',), []),
    'Перронный контроль': (('Авиационная безопасность',), []),
    'Охрана аэропорта ': (('Авиационная безопасность',), []),
    'Центровка и контроль загрузки ВС': (('Центровка и контроль загрузки',), []),
    'Организация наземного обслуживания ВС': (('Организация наземного обслуживания',), []),
    'Опасные грузы. 10 категория': ((), ['Программа повышения квалификации "Перевозка опасных грузов воздушным транспортом. 10 категория ИКАО/ИАТА. Базовый курс"', 'Программа повышения квалификации "Перевозка опасных грузов воздушным транспортом. 10 категория ИКАО/ИАТА"']),
    'Пассажирские перевозки': (('Организация\nпассажирских перевозок',), []),
    'Опасные грузы. 9 категория': ((), ['Программа повышения квалификации "Перевозка опасных грузов воздушным транспортом. 9 категория ИКАО/ИАТА. Базовый курс"', 'Программа повышения квалификации "Перевозка опасных грузов воздушным транспортом. 9 категория ИКАО/ИАТА"']),
    'DCS Астра': ((), []),
    'Опасные грузы. 8 категория': ((), ['Программа повышения квалификации "Перевозка опасных грузов воздушным транспортом. 8 категория ИКАО/ИАТА. Базовый курс"', 'Программа повышения квалификации "Перевозка опасных грузов воздушным транспортом. 8 категория ИКАО/ИАТА"']),
    'Безопасность полетов': (('Управление\n безопасностью полетов',), []),
}
# unused_disciplines = (('Подготовка преподавателей АУЦ', 'Противообледенительная\n защита ВС', 'Аварийно-спасательное обеспечение полетов', 'Водители'), ())

docx_dict = {
    'Программа повышения квалификации "Центровка и контроль загрузки воздушных судов. Базовый курс"': 'Центровка и контроль загрузки воздушных судов. Базовый курс.docx',
    'Программа повышения квалификации "Центровка и контроль загрузки воздушных судов"': 'Центровка и контроль загрузки воздушных судов.docx',
    'Программа повышения квалификации государственных гражданских служащих, осуществляющих деятельность  в системе  управления и контроля безопасности  полетов аэропорта по теме:"Система управления безопасностью полетов аэропортов"': 'Система управления безопасностью полетов аэропортов.docx',
    'Программа повышения квалификации  руководящего состава и специалистов поставщиков услуг по теме: "Система управления безопасностью полётов поставщиков услуг"': 'Система управления безопасностью полётов поставщиков услуг.docx',
    'Программа повышения квалификации "Базовые компетенции преподавателей Авиационных учебных центров"': 'Базовые компетенции преподавателей Авиационных учебных центров.docx',
    'Программа повышения квалификации "Подготовка преподавателей Авиационных учебных центров. Продвинутый курс"': 'Подготовка преподавателей авиационных учебных центров. Продвинутый курс.docx',
    'Программа повышения квалификации "Перевозка опасных грузов воздушным транспортом. 10 категория ИКАО/ИАТА. Базовый курс"': 'Перевозка опасных грузов воздушным транспортом. 10 категория ИКАО-ИАТА. Базовый курс.docx',
    'Программа повышения квалификации "Перевозка опасных грузов воздушным транспортом. 10 категория ИКАО/ИАТА"': 'Перевозка опасных грузов воздушным транспортом. 10 категория ИКАО-ИАТА.docx',
    'Программа повышения квалификации "Перевозка опасных грузов воздушным транспортом. 9 категория ИКАО/ИАТА. Базовый курс"': 'Перевозка опасных грузов воздушным транспортом. 9 категория ИКАО-ИАТА. Базовый курс.docx',
    'Программа повышения квалификации "Перевозка опасных грузов воздушным транспортом. 9 категория ИКАО/ИАТА"': 'Перевозка опасных грузов воздушным транспортом. 9 категория ИКАО-ИАТА.docx',
    'Программа повышения квалификации "Перевозка опасных грузов воздушным транспортом. 8 категория ИКАО/ИАТА. Базовый курс"': 'Перевозка опасных грузов воздушным транспортом. 8 категория ИКАО-ИАТА. Базовый курс.docx',
    'Программа повышения квалификации "Перевозка опасных грузов воздушным транспортом. 8 категория ИКАО/ИАТА"': 'Перевозка опасных грузов воздушным транспортом. 8 категория ИКАО-ИАТА.docx',
    'Программа повышения квалификации "Организация обслуживания пассажирских перевозок воздушным транспортом"': 'Организация обслуживания пассажирских перевозок воздушным транспортом.docx',
    'Программа повышения квалификации "Организация обслуживания пассажирских перевозок воздушным транспортом. Базовый курс"': 'Организация обслуживания пассажирских перевозок воздушным транспортом. Базовый курс.docx',
    'Программа повышения квалификации "Организация наземного обслуживания воздушных судов. Базовый курс"': 'Организация наземного обслуживания воздушных судов. Базовый курс.docx',
    'Программа повышения квалификации "Организация наземного обслуживания воздушных судов"': 'Организация наземного обслуживания воздушных судов.docx',
    'Программа повышения квалификации "Обеспечение противообледенительной защиты воздушных судов (категория по SAE AS6286А DI-L30). Базовый курс"': 'Обеспечение противообледенительной защиты ВС (категория по SAE AS6286A DI-L30). Базовый курс.docx',
    'Программа повышения квалификации "Обеспечение противообледенительной защиты воздушных судов (категория по SAE AS6286А DI-L30)"': 'Обеспечение противообледенительной защиты ВС (категория по SAE AS6286A DI-L30).docx',
    'Программа повышения квалификации "Организация и контроль противообледенительной защиты воздушных судов (категория по SAE AS6286А DI-L30B). Базовый курс"': 'Организация и контроль противообледенительной защиты ВС (категория по SAE AS6286A DI-L30В). Базовый курс.docx',
    'Программа повышения квалификации "Организация и контроль противообледенительной защиты воздушных судов (категория по SAE AS6286А DI-L30B)"': 'Организация и контроль противообледенительной защиты ВС (категория по SAE AS6286A DI-L30В).docx',
    'Программа повышения квалификации "Спасание и борьба с пожаром на воздушных судах и объектах аэропорта"': 'Спасание и борьба с пожаром на воздушных судах и объектах аэропорта.docx',
    'Программа начальной подготовки водителей спецтранспорта без права подъезда к воздушному в контролируемой зоне аэродрома "Пулково"': None,
    'Программа дополнительной подготовки водителей спецтранспорта без права подъезда к воздушному в контролируемой зоне аэродрома "Пулково"': None,
    'Программа начальной подготовки водителей спецтранспорта с правом подъезда к воздушному в контролируемой зоне аэродрома "Пулково"': None,
    'Программа дополнительной подготовки водителей спецтранспорта с правом подъезда к воздушному в контролируемой зоне аэродрома "Пулково"': None,
    'Программа начальной подготовки водителей спецтранспорта с правом эксплуатационного содержания летного поля в контролируемой зоне аэродрома "Пулково"': None,
    'Программа дополнительной подготовки водителей спецтранспорта с правом эксплуатационного содержания летного поля в контролируемой зоне аэродрома "Пулково"': None,
    'Программа начальной подготовки руководителей подъездом (отъездом) спецмашин к (от) воздушным судам на территории аэродрома "Пулково"': None,
    'Программа дополнительной подготовки руководителей подъездом (отъездом) спецмашин к (от) воздушным судам на территории аэродрома "Пулково"': None,
    'Программа начальной подготовки "Предполётный досмотр пассажиров, членов экипажей гражданских судов, обслуживающего персонала, ручной клади, багажа, грузов, почты и бортовых запасов"': 'Программа начальной подготовки «Предполетный досмотр пассажиров, членов ....docx',
    'Программа специальной профессиональной подготовки "Предполётный досмотр пассажиров, членов экипажей гражданских судов, обслуживающего персонала, ручной клади, багажа, грузов, почты и бортовых запасов"': None,
    'Программа повышения квалификации "Предполётный досмотр пассажиров, членов экипажей гражданских судов, обслуживающего персонала, ручной клади, багажа, грузов, почты и бортовых запасов"': 'Программа повышения квалификации «Предполетный досмотр пассажиров, члено....docx',
    'Программа начальной подготовки "Перронный контроль и досмотр воздушных судов"': 'Программа начальной подготовки «Перронный контроль и досмотр воздушных с....docx',
    'Программа специальной профессиональной подготовки "Перронный контроль и досмотр воздушных судов"': 'Программа специальной профессиональной подготовки «Перронный контроль и ....docx',
    'Программа повышения квалификации "Перронный контроль и досмотр воздушных судов"': 'Программа повышения квалификации «Перронный контроль и досмотр воздушных....docx',
    'Программа начальной подготовки "Предотвращение несанкционированного доступа в контролируемую зону аэропорта"': 'Программа начальной подготовки «Предотвращение несанкционированного Дост....docx',
    'Программа специальной профессиональной подготовки  "Предотвращение несанкционированного доступа в контролируемую зону аэропорта"': None,
    'Программа повышения квалификации "Предотвращение несанкционированного доступа в контролируемую зону аэропорта"': 'Программа повышения квалификации «Предотвращение несанкционированного до....docx',
    'Программа повышения квалификации "Перевозка опасных грузов воздушным транспортом. 12 категория ИКАО/ИАТА"': None,
    'Аварийно-спасательное обеспечение полетов': None
}

for k in disciplines_dict:
    curs = disciplines_dict[k][1]
    for disc in disciplines_dict[k][0]:
        disc_row_start = curriculum_pars.index[curriculum_pars.iloc[:, 1] == disc].tolist()[0]
        disc_row_end = disc_row_start
        while True:
            disc_row_end += 1
            if disc_row_end == len(curriculum_pars) or curriculum_pars.iloc[disc_row_end, 1] != None:
                break
        curs.append(list(curriculum_pars.iloc[disc_row_start:disc_row_end, 1]))
    list(map(lambda x: (x[0], curriculum_pars.index[curriculum_pars.iloc[:, 2] == x[0]].tolist()[0] + 1), curs))
    disciplines_dict[k] = curs

# docx2csv
for c in currics:
    if c.specialization not in disciplines_dict: continue
    c.theme = disciplines_dict[c.specialization].pop(0)
    c.plan, c.calendar = read_docx_tables('data/Приложение №3 (2)/' + docx_dict[c.theme[0]])
    c.pick_lecturers_and_auditories()
