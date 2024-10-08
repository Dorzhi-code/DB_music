"""
filling_tables
"""

from yoyo import step

__depends__ = {'20241006_01_iJqeh-reate-neighborhood-tree'}

steps = [
    step('''
    INSERT INTO neighborhood_tree (id, title, parent_id)
    VALUES
         (1, 'Каталог товаров', NULL),
         (2, 'Бытовая техника', 1),
         (3, 'Красота и здоровье', 1),
         (4, 'Смартфоны и фототехника', 1),
         (5, 'Встраиваемая техника', 2),
         (6, 'Техника для кухни', 2),
         (7, 'Техника для дома', 2),
         (8, 'Укладка и сушка волос', 3),
         (9, 'Бритье, стрижка и эпиляция', 3),
         (10, 'Уход за полостью рта', 3),
         (11, 'Уход за телом', 3),
         (12, 'Смартфоны и гаджеты', 4),
         (13, 'Планшеты, электронные книги', 4),
         (14, 'Фототехника', 4),
         (15, 'Варочные панели', 5),
         (16, 'Духовые шкафы', 5),
         (17, 'Вытяжки', 5),
         (18, 'Встраиваемые микроволновые печи', 5),
         (19, 'Встраиваемые холодильники', 5),

         (20, 'Плиты и печи', 6),
         (21, 'Холодильное оборудование', 6),
         (22, 'Посудомоечные машины', 6),
         (23, 'Приготовление напитков', 6),
         (24, 'Электрочайники и термопоты', 6),

         (25, 'Стирка и сушка', 7),
         (26, 'Глаженье', 7),
         (27, 'Уборка', 7),
         (28, 'Водонагреватели и котлы отопления', 7),
         (29, 'Летний климат', 7), 
         (30, 'Фены', 8),
         (31, 'Фены-щетки', 8),
         (32, 'Щипцы для волос', 8),
         (33, 'Выпрямители для волос', 8),
         (34, 'Мультистайлеры', 8),
         (35, 'Триммеры', 9), 
         (36, 'Машинки для стрижки волос', 9),
         (37, 'Мужские электробритвы', 9),
         (38, 'Эпиляторы', 9),
         (39, 'Аксессуары к бритвам', 9),
         (40, 'Электрические зубные щетки', 10),
         (41, 'Ирригаторы', 10),
         (42, 'Насадки для зубных щеток и ирригаторов', 10),
         (43, 'Футляры для зубных щеток', 10),
         (44, 'Держатели для зубных щеток', 10),
         (45, 'Массажеры', 11),
         (46, 'Массажные ванночки', 11),
         (47, 'Весы напольные', 11),
         (48, 'Весы детские', 11),
         (49, 'Материнство и детство', 11),
         (50, 'Смартфоны', 12),
         (51, 'Смарт-часы и браслеты', 12),
         (52, 'Детские часы', 12),
         (53, 'Планшеты', 13),
         (54, 'Электронные книги', 13),
         (55, 'Цифровые блокноты', 13),
         (56, 'Фотоаппараты', 14),
         (57, 'Экшн-камеры', 14),
         (58, 'Квадрокоптеры с камерами', 14),
         (59, 'Видеокамеры', 14),
         (60, 'Объективы', 14),
         (61, 'Варочные панели электрические', 15),
         (62, 'Варочные панели индукционные', 15),
         (63, 'Варочные панели газовые', 15),
         (64, 'Варочные панели комбинированные', 15),
         (65, 'Аксессуары к варочным панелям', 15),
         (66, 'Духовые шкафы электрические', 16),
         (67, 'Духовые шкафы газовые', 16),
         (68, 'Аксессуары к духовым шкафам', 16),
         (69, 'Вытяжки', 17),
         (70, 'Полновстраиваемые вытяжки', 17),
         (71, 'Телескопические вытяжки', 17),
         (72, 'Каминные вытяжки', 17),
         (73, 'Встраиваемая микроволновая печь Zigmund & Shtain BMO 16.202 W белый', 18),
         (74, 'Встраиваемая микроволновая печь DEXP BLD25SS серебристый', 18),
         (75, 'Встраиваемая микроволновая печь DEXP B21BB черный', 18),
         (76, 'Встраиваемая микроволновая печь Korting KMI 825 TGB бежевый', 18),
         (77, 'Встраиваемый холодильник без морозильника DEXP BIS2-0140AHE', 19),
         (78, 'Встраиваемый холодильник DEXP BIB4-0250AHE', 19),
         (79, 'Встраиваемый холодильник DEXP BIB220AMA', 19),
         (80, 'Встраиваемый холодильник без морозильника LEX RBI 102 DF', 19),
         (81, 'Плиты электрические', 20),
         (82, 'Плиты газовые', 20),
         (83, 'Плиты комбинированные', 20),
         (84, 'Настольные газовые плиты', 20),
         (85, 'Настольные электрические плиты', 20),
         (86, 'Холодильники', 21),
         (87, 'Холодильные витрины', 21),
         (88, 'Встраиваемые холодильники', 21),
         (89, 'Посудомоечные машины', 22),
         (90, 'Встраиваемые посудомоечные машины', 22),
         (91, 'Френч-прессы', 23)
         ''')
]
