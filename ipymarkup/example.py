# coding: utf-8
from __future__ import unicode_literals

from .utils import Record
from .markup import Ascii, Html
from .color import register as register_color
from . import *


__all__ = [
    'TEXT1',
    'SPANS1',
    'TEXT2',
    'SPANS2',
    'TEXT3',
    'SPANS3',
    'TEXT4',
    'SPANS4',
    'TEXT5',
    'SPANS5',
    'TEXT6',
    'SPANS6',
]


def is_space(char):
    import re
    return re.match(r'\s', char)


def generate_spans(text):
    mins = {}
    maxes = {}
    for index, char in enumerate(text):
        if is_space(char):
            continue
        if char not in mins:
            mins[char] = index
        maxes[char] = index
    for char in mins:
        if char in maxes:
            start = mins[char]
            stop = maxes[char] + 1
            yield Span(start, stop, type=char)


def generate_cases():
    text = 'a a a b b c c c'
    spans = list(generate_spans(text))
    yield text, spans

    text = 'a a a b b c e d d d f f g g h'
    spans = list(generate_spans(text))
    yield text, spans

    text = 'a d a b a a a b c c c f d'
    spans = list(generate_spans(text))
    yield text, spans

    text = 'a b b c c d e f g h h i i a'
    spans = list(generate_spans(text))
    yield text, spans


MARKUPS = [
    BoxMarkup,
    BoxLabelMarkup,
    LineMarkup,
    LineLabelMarkup,
    AsciiMarkup
]

TYPES = 'abcdefghijklmno'


def init_colors():
    register_color(None)
    for type in TYPES:
        register_color(type)


def generate_cell(markup):
    if isinstance(markup, Html):
        for line in markup.as_html:
            yield line
    elif isinstance(markup, Ascii):
        yield '<pre>'
        yield '\n'.join(markup.as_ascii)
        yield '</pre>'


def generate_row(case):
    text, spans = case
    for Markup in MARKUPS:
        markup = Markup(text, spans)
        yield ''.join(generate_cell(markup))


def generate_header():
    for markup in MARKUPS:
        yield markup.__name__


def generate_table():
    init_colors()
    yield generate_header()
    for case in generate_cases():
        yield generate_row(case)


def format_table(rows):
    yield '<table>'
    for row in rows:
        yield '<tr style="background: none">'
        for cell in row:
            yield '<td style="width: 20%">'
            yield cell
            yield '</td>'
        yield '</tr>'
    yield '</table>'


def show_html(lines):
    from IPython.display import display, HTML

    html = '\n'.join(lines)
    display(HTML(html))


def show_table():
    rows = generate_table()
    html = format_table(rows)
    show_html(html)


TEXT1 = 'Так говорила в июле 1805 года известная Анна Павловна Шерер, фрейлина и приближенная императрицы Марии Феодоровны, встречая важного и чиновного князя Василия, первого приехавшего на ее вечер. Анна Павловна кашляла несколько дней, у нее был грипп, как она говорила (грипп был тогда новое слово, употреблявшееся только редкими).'

SPANS1 = [
    Span(15, 29, 'Date'),
    Span(40, 59, 'Name'),
    Span(97, 113, 'Name'),
    Span(150, 157, 'Name'),
    Span(192, 205, 'Name')
]


TEXT2 = '''	  


	 Кустов Дмитрий Владимирович
Мужчина, 35 лет, родился 7 августа 1979

+7 (926) 217-87-15 - желаемый способ связи
+7 (926) 565-91-98
dvkustov@gmail.com
Skype: dkustov

Проживает: Москва, м. Савеловская
Гражданство: Россия, есть разрешение на работу: Россия
Не готов к переезду, готов к командировкам

	Желаемая должность и зарплата

	CIO, CTO, Руководитель отдела разработки программного обеспечения
Информационные технологии, интернет, телеком
• Управление проектами
• Программирование, Разработка
• CTO, CIO, Директор по IT

Занятость: полная занятость
График работы: полный день

Желательное время в пути до работы: не имеет значения
...
'''

SPANS2 = [
    Span(8, 35, 'NAME'),
    Span(36, 43, 'GENDER'),
    Span(53, 75, 'BIRTH'),
    Span(77, 95, 'PHONE'),
    Span(120, 138, 'PHONE'),
    Span(139, 157, 'EMAIL'),
    Span(174, 207, 'LIVES_AT'),
    Span(208, 227, 'CITIZENSHIP'),
    Span(229, 262, 'PERMISSION'),
    Span(263, 282, 'RELOCATION'),
    Span(284, 305, 'TRAVEL'),
    Span(340, 405, 'POSITION'),
    Span(406, 450, 'SECTION'),
    Span(451, 473, 'SUBSECTION'),
    Span(474, 504, 'SUBSECTION'),
    Span(505, 531, 'SUBSECTION'),
    Span(533, 560, 'EMPLOYMENT'),
    Span(561, 587, 'SCHEDULE'),
    Span(589, 642, 'COMMUTE'),
]

TEXT3 = '''Р Е Ш Е Н И Е 
г. Москва      дело № А40-253826/16-58-1617 
«02» мая 2017г.     
Резолютивная часть решения объявлена 13.03.2017г. 
Решение в полном объеме изготовлено 02.05.2017г. 
Арбитражный суд г. Москвы в составе: 
судьи О.Н. Жура, 
при секретаре Поддубном Е.О.,  
рассмотрев в судебном заседании дело по исковому заявлению ООО «Экопром» (ОГРН 
1055255024912, 117042, г. Москва, б-р Адмирала Ушакова, д. 18, кв. 287) к ответчику ГБУ 
г. Москвы «Ритуал» (ОГРН 1157746320555, 125057, г. Москва, ул. Песчаная, д.3) о 
взыскании задолженности, 
по встречному исковому заявлению ГБУ г. Москвы «Ритуал» к ответчику - ООО 
«Экопром» о взыскании пени в размере 932.393, 94 руб., штрафа по государственному 
контракту №0373200657316000007-44/2016 от 21.06.2016 г. в размере 625.157, 31 руб. 
с участием: представитель истца - Чекин Р.О. (паспорт, доверенность от 01.09.2016 г.), 
представитель ответчика - Рябова И.А. (паспорт, доверенность от 20.02.2017 г.), '''

SPANS3 = [
    Span(631, 674, 'topic'),
    Span(517, 543, 'topic'),
    Span(549, 578, 'topic'),
    Span(310, 328, 'topic'),
    Span(30, 34, 'topic'),
    Span(302, 306, 'topic'),
    Span(182, 235, 'staff'),
    Span(434, 457, 'claim'),
    Span(579, 601, 'claim'),
    Span(658, 674, 'claim'),
    Span(770, 786, 'claim'),
    Span(902, 913, 'claim'),
    Span(226, 235, 'claim'),
    Span(252, 266, 'claim'),
    Span(822, 832, 'claim'),
    Span(329, 342, 'claim'),
    Span(616, 630, 'claim'),
    Span(549, 578, 'claim'),
    Span(128, 139, 'claim'),
    Span(178, 193, 'claim'),
    Span(198, 207, 'claim'),
    Span(373, 382, 'claim'),
    Span(487, 496, 'claim'),
    Span(310, 328, 'claim'),
    Span(788, 798, 'claim'),
    Span(344, 363, 'claim'),
    Span(459, 477, 'claim'),
    Span(686, 713, 'claim'),
    Span(302, 306, 'claim'),
    Span(814, 819, 'claim'),
    Span(424, 433, 'claim'),
    Span(604, 613, 'claim'),
    Span(890, 899, 'claim'),
    Span(422, 423, 'claim'),
    Span(602, 603, 'claim'),
    Span(517, 518, 'claim'),
    Span(631, 632, 'claim'),
    Span(520, 529, 'claim'),
    Span(633, 642, 'claim'),
    Span(530, 543, 'claim'),
    Span(643, 647, 'claim'),
    Span(676, 682, 'claim'),
    Span(100, 107, 'claim'),
    Span(743, 759, 'outcome'),
    Span(856, 872, 'outcome'),
    Span(937, 953, 'outcome'),
    Span(252, 266, 'outcome'),
    Span(822, 832, 'outcome'),
    Span(902, 913, 'outcome'),
    Span(226, 235, 'outcome'),
    Span(788, 798, 'outcome'),
    Span(800, 813, 'outcome'),
    Span(876, 889, 'outcome'),
    Span(424, 433, 'outcome'),
    Span(604, 613, 'outcome'),
    Span(890, 899, 'outcome'),
    Span(814, 819, 'outcome'),
    Span(843, 855, 'outcome'),
    Span(924, 936, 'outcome')
]

TEXT4 = '''Опыт работы - 28 лет 8 месяцев
Январь 2010 -
Март 2016
6 лет 3 месяца

ООО ТрансРоуд
Москва

старший мастер по ремонту автотранспорта
контроль за выполнением качественного ремонта автотранспорта,проведением ТО,
руководство персоналом АРМ,соблюдением норм техники безопасности и охраны труда

Январь 1994 -
Январь 2004
10 лет 1 месяц

ГУП Тереньгульское АТП
Ульяновская область

Главный инженер
руководство производственной деятельностью АТП, руководство коллективом,

Сентябрь 1981 -
Январь 1994
12 лет 5 месяцев

Автотранспортное предприятие 10 ГлавТашкентстроя
начальник эксплуатации, начальник коллонны
распределение автотранспорта, по организациям, контроль за трудовой дисциплиной
водителей, выполнением сменных заданий водителями, руководство коллективом

'''

SPANS4 = [
    Span(0, 30, 'PERIOD'),
    Span(31, 69, 'COMPANY'),
    Span(71, 84, 'COMPANY'),
    Span(85, 91, 'LOCATION'),
    Span(93, 133, 'POSITION'),
    Span(134, 290, 'DESCRIPTION'),
    Span(292, 332, 'PERIOD'),
    Span(334, 356, 'COMPANY'),
    Span(357, 376, 'LOCATION'),
    Span(378, 393, 'POSITION'),
    Span(394, 466, 'DESCRIPTION'),
    Span(468, 512, 'PERIOD'),
    Span(514, 562, 'COMPANY'),
    Span(563, 605, 'POSITION'),
    Span(606, 760, 'DESCRIPTION'),
    Span(31, 290, 'JOB'),
    Span(468, 760, 'JOB'),
    Span(292, 466, 'JOB')
]

TEXT5 = 'Секретарь Совета национальной безопасности и обороны (СНБО) Андрей Парубий не исключил скорого введения военного положения в Донбассе. Как сообщает «Интерфакс», он уточнил, что речь идет непосредственно о Донецкой и Луганской областях. По словам Парубия, документ о введении военного положения уже подготовлен ведомством. Он предусматривает не только указ президента Украины Петра Порошенко, но и «координацию и систему управления всех наших подразделений в новой системе координат». Комментируя информацию о возможном введении российских миротворцев на восток страны, Парубий заявил, что эти действия представляют собой прямую агрессию в отношении Украины, сообщает «Сегодня.ua». Он подчеркнул, что решение о введении миротворцев должно приниматься под эгидой ООН. Секретарь СНБО также заявил, что, по его информации, у границы с Украиной дислоцировано около 40 тысяч российских военных. «Опасность штурма есть с первого дня Майдана и не снижалась никогда»,  — резюмировал он. 1 июля парламентская коалиция Верховной Рады потребовала от Порошенко ввести военное положение на востоке Украины, однако спикер парламента Александр Турчинов заявил, что немедленное рассмотрение вопроса невозможно. «Военное положение вводится исключительно указом Президента, и в течение двух дней Рада должна одобрить этот указ», — заявил он. В начале июня Турчинов, исполнявший тогда обязанности главы государства, допускал возможность введения военного положения. Принятие решения, однако, было отложено до инаугурации Порошенко. Он со своей стороны поддержал продолжение силовой операции на востоке, одновременно заявив о необходимости прекращения огня в течение недели.'

SPANS5 = [
    Span(60, 66, 'NAME'),
    Span(67, 74, 'NAME'),
    Span(375, 390, 'NAME'),
    Span(1008, 1022, 'NAME'),
    Span(1038, 1047, 'NAME'),
    Span(1118, 1136, 'NAME'),
    Span(1501, 1510, 'NAME')
]

TEXT6 = 'a d a b a a a b c c c f d'
SPANS6 = list(generate_spans(TEXT6))
