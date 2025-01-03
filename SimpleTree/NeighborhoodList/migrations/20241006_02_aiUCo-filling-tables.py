"""
filling_tables
"""

from yoyo import step

__depends__ = {'20241006_01_iJqeh-reate-neighborhood-tree'}

steps = [
    step('TRUNCATE neighborhood_tree'),   
    step('''
    INSERT INTO neighborhood_tree (id, title, parent_id)
    VALUES
         (1, 'Каталог товаров', NULL),
         (2, 'Бытовая техника', 1),
         (3, 'Красота и здоровье', 1),
         (4, 'Встраиваемая техника', 2),
         (5, 'Техника для кухни', 2),
         (6, 'Укладка и сушка волос', 3),
         (7, 'Бритье, стрижка и эпиляция', 3),
         (8, 'Варочные панели', 4),
         (9, 'Духовые шкафы', 4),
         (10, 'Плиты и печи', 5),
         (11, 'Холодильное оборудование', 5),         
         (12, 'Фены', 6),
         (13, 'Фены-щетки', 6),         
         (14, 'Триммеры', 7),
         (15, 'Машинки для стрижки волос', 7),         
         (16, 'Варочные панели электрические', 8),
         (17, 'Варочные панели индукционные', 8),        
         (18, 'Духовые шкафы электрические', 9),
         (19, 'Духовые шкафы газовые', 9),         
         (20, 'Плиты электрические', 10),
         (21, 'Плиты газовые', 10),
         (22, 'Холодильники', 11),
         (23, 'Холодильные витрины', 11),
         (24, 'Фен Aceline BA-100 красный/черный', 12),
         (25, 'Фен Kitfort КТ-3243-1 желтый/черный', 12),
         (26, 'Фен Kitfort КТ-3244-2 оранжевый/черный', 12),
         (27, 'Фен-щетка DEXP HB-801NR черный/красный', 13),
         (28, 'Фен-щетка Aceline HB-801NR черный/красный', 13),
         (29, 'Фен-щетка DEXP HB-1001NR черный/розовый', 13),
         (30, 'Триммер Aceline NT-01WP серебристый/черный', 14),
         (31, 'Триммер DEXP NT-01WP серебристый/черный', 14),
         (32, 'Машинка для стрижки MercuryHaus MC-6787 белый/оранжевый', 15),
         (33, 'Машинка для стрижки HTC AT-202 белый/золотистый', 15),
         (34, 'Электрическая варочная поверхность DEXP 4M2CTYL/B', 16),
         (35, 'Индукционная варочная поверхность HOMSair HI32ABK', 16),
         (36, 'Индукционная варочная поверхность HOMSair IH32KAB', 17),
         (37, 'Индукционная варочная поверхность DEXP EH-I2SMA/B', 17),
         (38, 'Электрический духовой шкаф DEXP 1M70GNB черный', 18),
         (39, 'Электрический духовой шкаф Gefest ДА 602 К2 черный', 18),
         (40, 'Газовый духовой шкаф Gefest ДГЭ 621-03 Б1', 19),
         (41, 'Газовый духовой шкаф Korting OGG 541 CFX', 19),
         (42, 'Электрическая плита Мечта 15М белый', 20),
         (43, 'Электрическая плита FLAMA CE 32011 B коричневый', 20),
         (44, 'Газовая плита Flama NP CG 32020 В коричневый', 21),
         (45, 'Газовая плита Aceline G15-1W белый', 21),
         (46, 'Холодильник косметический Kitfort КТ-4104 зеленый', 22),
         (47, 'Холодильник компактный DEXP RF-SD070MA/W белый', 22),
         (48, 'Холодильная витрина Бирюса 102 белый', 23),
         (49, 'Холодильная витрина DEXP GS2-5090AMG черный', 23)

         '''),
    step('''
        ALTER SEQUENCE neighborhood_tree_id_seq RESTART WITH 50;
         '''),
]
