# для работы со временем:
from datetime import datetime
from time import time

# импортировать другие файлы проекта:
from operations_with_files import *

# импортировать необходимый набор словарей с экипировкой:
from equipment_custom import *
#from equipment_wow_classic import *
#from equipment_obvious_strong import *
#from equipment_obvious_weak import *


class Rogue:
    """Класс описывает механику тестируемого персонажа."""

    def __init__(self):

        # инициализация списка слотов экипировки, который должен содержать id надетых предметов:
        # 0 - правая рука, 1 - левая рука, 2 - перчатки, 3 - голова, 4 - грудь, 5 - штаны, 6 - обувь
        self.equipment_slots = [0] * 7

        # инициализация списка слотов экипировки, который должен содержать названия надетых предметов:
        self.equipment_names = ['ничего'] * 7

        # БАЗОВЫЕ значения характеристик (они - точка отсчёта при смене экипировки):
        self.basic_stat_agility = 50
        self.basic_stat_power = 40
        self.basic_stat_hit = 80
        self.basic_stat_crit = 20
        self.basic_stat_mastery = 0

        # рассчитать текущие характеристики без вещей:
        self.set_stats_without_equip()


    # метод для расчёта текущих характеристик без вещей:
    def set_stats_without_equip(self):
        self.stat_agility = self.basic_stat_agility
        self.stat_power = self.basic_stat_power
        self.stat_attackpower = self.stat_agility + self.stat_power
        self.stat_hit = self.basic_stat_hit
        self.direct_crit_bonus = 0
        self.calculate_critical_percent()
        self.stat_mastery = self.basic_stat_mastery
        self.calculate_glancing_percent()

    # метод для расчёта шанса критического удара:
    def calculate_critical_percent(self):
        self.stat_crit = self.basic_stat_crit + self.direct_crit_bonus + self.stat_agility // 20

    # метод для расчёта шанса скользящего удара:
    def calculate_glancing_percent(self):
        self.stat_glancing_percent = 40 - self.stat_mastery * 4


    # переопределяем "магический метод" для демонстрации текущего состояния персонажа:
    def __str__(self):

        # выписать в строку названия надетых предметов:
        using_equipment_names = ''
        for i in range(0, len(self.equipment_names) - 1 ):
            using_equipment_names += self.equipment_names[i] + '", "'
        using_equipment_names = '"' + using_equipment_names + self.equipment_names[-1] + '"'

        # удобочитаемый текст:
        description = 'Разбойник 60 уровня\n'
        description += using_equipment_names + '\n'
        description += 'сила атаки: ' + str(self.stat_attackpower) + ' ед.\n'
        description += 'ловкость: ' + str(self.stat_agility) + ' ед.\n'
        description += 'сила: ' + str(self.stat_power) + ' ед.\n'
        description += 'меткость: ' + str(self.stat_hit) + '%\n'
        description += 'крит. шанс: ' + str(self.stat_crit) + '%\n'
        description += 'мастерство: ' + str(self.stat_mastery) + ' ед.\n'
        description += 'шанс скольз. уд.: ' + str(self.stat_glancing_percent) + '%\n'
        return description


    # метод для "снятия всей экипировки":
    def unwear_all(self):
        # сбросить id и названия экипировки на слотах персонажа:
        for i in range(0, len(self.equipment_slots) ):
            self.equipment_slots[i] = 0
            self.equipment_names[i] = 'ничего'

        self.set_stats_without_equip()


    # метод для надевания экипировки:
    def wear_item(self, slot, item_id, items_list):

        # в слоте не должно быть экипировки, иначе пришлось бы снять её и отнять характеристики, которые она дала:
        if self.equipment_slots[slot] == 0:
            self.equipment_slots[slot] = item_id
            self.equipment_names[slot] = items_list[item_id][0]
            self.stat_agility += items_list[item_id][2]
            self.stat_power += items_list[item_id][3]
            # не забываем, что к силе атаки нужно добавить бонусы также от силы и ловкости:
            self.stat_attackpower += items_list[item_id][1] + items_list[item_id][2] + items_list[item_id][3]
            self.stat_hit += items_list[item_id][4]
            self.direct_crit_bonus += items_list[item_id][5]
            self.stat_mastery += items_list[item_id][6]

            # если была добавлена ловкость ИЛИ прямой бонус к крит. шансу, пересчитать общий крит. шанс:
            if items_list[item_id][2] != 0 or items_list[item_id][5] != 0:
                self.calculate_critical_percent()

            # если было добавлено мастерство, пересчитать вероятность скользящего удара:
            if items_list[item_id][6] != 0:
                self.calculate_glancing_percent()

            # особый случай для набора экипировки "custom":
            if EQUIPMENT_COLLECTION == 'custom':
                # если в левую руку взят "Леворучный Страж Лесов" (id 1 для слота "левая рука"),
                # а в правую взят "Праворучный Страж Лесов" (id 1 для слота "правая рука"),
                # добавить дополнительно 2 к крит. шансу:
                if slot == 1:
                    if self.equipment_slots[1] == 1 and self.equipment_slots[0] == 1:
                        self.direct_crit_bonus += 2
                        self.calculate_critical_percent()
                        print('Дары Лесов вместе...')

            # особые случаи для набора экипировки "wow classic preraid":
            if EQUIPMENT_COLLECTION == 'wow_classic_preraid':
                # если в левую руку взят "Племенной страж Дал'Ренда" (id 1 для этого слота),
                # а в правую уже взят "Священный заряд Дал'Ренда" (id 1 для этого слота),
                # добавить дополнительно 50 к силе атаки:
                if slot == 1:
                    if self.equipment_slots[1] == 1 and self.equipment_slots[0] == 1:
                        self.stat_attackpower += 50
                        print('Дал\'Ренды соединились вновь...')

                # если надеты штаны "Поножи девизавра" (id 1 для этого слота),
                # вместе с перчатками "Рукавицы девизавра" (id 1 для этого слота),
                # добавить дополнительно 2 к крит. шансу:
                if slot == 5:
                    if self.equipment_slots[2] == 1 and self.equipment_slots[5] == 1:
                        self.direct_crit_bonus += 2
                        self.calculate_critical_percent()
                        print('Сила девизавра едина...')


# провести сессию тестов набора экипировки:
def run_session(SESSION_LOG):

    # счётчик рассчитанных ожиданий:
    expectation_number = 1

    # здесь будут накапливаться отчёты:
    all_reports = ''

    # для каждого оружия в правой руке:
    for new_righthand_id in RIGHT_HANDS:
        # для каждого оружия в левой руке:
        for new_lefthand_id in LEFT_HANDS:
            # для каждых перчаток:
            for new_gloves_id in GLOVES:
                # для каждого шлема:
                for new_head_id in HEADS:
                    # для каждого нагрудника:
                    for new_chest_id in CHESTS:
                        # для каждых штанов:
                        for new_pants_id in PANTS:
                            # для каждой обуви:
                            for new_boots_id in BOOTS:

                                new_calculation = test_combination(expectation_number,
                                                                  new_righthand_id,
                                                                  new_lefthand_id,
                                                                  new_gloves_id,
                                                                  new_head_id,
                                                                  new_chest_id,
                                                                  new_pants_id,
                                                                  new_boots_id
                                                                  )

                                all_reports += new_calculation
                                expectation_number += 1

    # записать результаты расчётов в этом сеансе:
    save_data_to_file(SESSION_LOG, all_reports)


# подготовка к следующему расчёту и его запуск:
def test_combination(expectation_number, righthand_id, lefthand_id, gloves_id, head_id, chest_id, pants_id, boots_id):

    # сбросить все вещи:
    my_rogue.unwear_all()

    # взять оружие в правую руку:
    my_rogue.wear_item(0, righthand_id, RIGHT_HANDS)

    # взять оружие в левую руку:
    my_rogue.wear_item(1, lefthand_id, LEFT_HANDS)

    # надеть перчатки:
    my_rogue.wear_item(2, gloves_id, GLOVES)

    # надеть наголовник:
    my_rogue.wear_item(3, head_id, HEADS)

    # надеть нагрудник:
    my_rogue.wear_item(4, chest_id, CHESTS)

    # надеть поножи:
    my_rogue.wear_item(5, pants_id, PANTS)

    # надеть обувь:
    my_rogue.wear_item(6, boots_id, BOOTS)


    # выписать в строку "профайл" эквипа:
    equipment_profile = str(righthand_id) + ',' + str(lefthand_id) + ',' + str(gloves_id) + \
                            ',' + str(head_id) + ',' + str(chest_id) + ',' + str(pants_id) + \
                            ',' + str(boots_id)

    print(my_rogue)
    print('equipment_profile =', equipment_profile)

    # рассчитать математическое ожидание для текущего эквипа:
    return calculate_expectation(equipment_profile, expectation_number)


# рассчитать математическое ожидание:
def calculate_expectation(equipment_profile, expectation_number):

    # вычислить вероятность попадания:
    p_hit = my_rogue.stat_hit / 100

    # вычислить вероятность скользящего и НЕскользящего удара:
    p_glancing = my_rogue.stat_glancing_percent / 100
    not_p_glancing = 1 - my_rogue.stat_glancing_percent / 100

    # вычислить вероятность критического и НЕкритического удара:
    p_crit = my_rogue.stat_crit / 100
    not_p_crit = 1 - my_rogue.stat_crit / 100

    # вычислить ожидание модификатора:
    expectation_modificator = p_hit * ( p_glancing * 0.7 + not_p_glancing * ( p_crit * 2 + not_p_crit ))

    # вычислить ожидание урона с таким модификатором:
    expectation_damage = expectation_modificator * my_rogue.stat_attackpower
    expectation_damage = round(expectation_damage, 3)

    print('ожидание модификатора =', expectation_modificator)
    print('ожидание урона =', expectation_damage)

    result = '#' + str(expectation_number) + '/' + equipment_profile + '/' + str(expectation_damage) + '/' + str(expectation_modificator) + '\n'
    return result


# вывести указанное количество комбинаций с максимальным уроном:
def show_best_sets(SESSION_LOG, number_of_sets):

    # список для хранения результатов расчётов:
    list_log = list()

    # прочитать строки лога, выписав из них в список list_log кортежи,
    # содержащие сумму нанесённого урона и используемый для этого профиль экипировки:
    with open(SESSION_LOG, 'r', encoding='utf8') as f:
        lines = f.readlines()
        for line in lines:
            try:
                list_line = line.split('/')
                list_log.append( ( float(list_line[2]), list_line[1].split(',') ) )
            except IndexError:
                break

    # сортировать список, чтобы лучшие результаты оказались в начале:
    list_log.sort(reverse=True)

    # сформировать удобочитаемый отчёт, перебрав number_of_sets кейсов в списке лучших результатов:
    top_sets_info = ''
    for i in range(0, number_of_sets):
        current_case = list_log[i]

        # перебрать список идентификаторов экипировки в текущем кейсе и выписать их названия:
        clear_report = ''
        equipment_names = ''
        equip_group = 1

        for equip_id in current_case[1]:
            equipment_names += '\n' + get_equip_name(equip_id, equip_group)
            equip_group += 1

        line_for_clear_report = '\n#' + str(i+1) + ' - ожид. урон ' + str(current_case[0]) + ' у набора:' + equipment_names
        clear_report += line_for_clear_report

        print('\n', clear_report)
        top_sets_info += clear_report + '\r'

    return top_sets_info


# вывести название экипировки по id:
def get_equip_name(equip_id, equip_group):
    equip_id = int(equip_id)

    if equip_group == 1:
        return RIGHT_HANDS[equip_id][0]
    if equip_group == 2:
        return LEFT_HANDS[equip_id][0]
    if equip_group == 3:
        return GLOVES[equip_id][0]
    if equip_group == 4:
        return HEADS[equip_id][0]
    if equip_group == 5:
        return CHESTS[equip_id][0]
    if equip_group == 6:
        return PANTS[equip_id][0]
    if equip_group == 7:
        return BOOTS[equip_id][0]



# ЗАПУСК:
if __name__ == "__main__":

    # сгенерировать название лога тестовой сессии:
    SESSION_LOG = 'session_logs/for ' + EQUIPMENT_COLLECTION + ' results ' + datetime.strftime(datetime.now(), '%Y-%m-%d_%H-%M-%S') + '.txt'
    print('SESSION_LOG =', SESSION_LOG)

    # создать персонажа:
    my_rogue = Rogue()

    # засечь время:
    time_begin = time()

    # запустить тестовую сессию:
    run_session(SESSION_LOG)

    # вычислить затраченное время:
    time_session = time() - time_begin
    duration_info = 'сессия длилась: ' + str( round(time_session, 3) ) + ' сек.'
    print('\n' + duration_info)
    append_data_to_file(SESSION_LOG, duration_info + '\n')

    # проанализировать сессию, с выводом 5 самых лучших сочетаний экипировки:
    top_sets_info = show_best_sets(SESSION_LOG, 5)

    # записать отчёт о лучших результатах в тот же общий файл:
    append_data_to_file(SESSION_LOG, top_sets_info)

else:
    print('__name__ is not "__main__".')
