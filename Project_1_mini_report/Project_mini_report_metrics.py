#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import vk_api
import random

ads = pd.read_csv('ads_data_121288.csv')

ads_views = ads[ads['event']=='view'].groupby(['date','ad_id']).count().reset_index()[['date','ad_id', 'event']]
ads_views.columns ['date','ad_id', 'views']

ads_clicks = ads[ads['event']=='click'].groupby(['date','ad_id']).count().reset_index()[['date','ad_id', 'event']]
ads_clicks.columns['date','ad_id', 'clicks']

# Объединяем таблицы по 'date'и 'ad_id'
ads_ctr = pd.merge(ads_views, ads_clicks, on = ['date', 'ad_id'])

# CTR (отношение кликов к показам), добавляем новый столбец
ads_ctr['CTR'] = ads_ctr['event_y']/ads_ctr['event_x']*100

# Рассчёт суммы потраченных денег по формуле:
# Значение из колонки ad_cost разделить на 1000 и умножить на количество показов объявления.
ads['ad_action_cost']=ads['ad_cost']/1000

# Стоимость затрат: показы *стоимость действия
ads_ctr['money'] = ads_ctr['event_x']*ads['ad_action_cost'].unique()[0]

#Метрики за 02.04.2019
money_0204=float (ads_ctr[ads_ctr['date']=='2019-04-02']['money'])
view_0204=float (ads_ctr[ads_ctr['date']=='2019-04-02']['event_x'])
clicks_0204=float (ads_ctr[ads_ctr['date']=='2019-04-02']['event_y'])
ctr_0204=float (ads_ctr[ads_ctr['date']=='2019-04-02']['CTR'])

#Метрики за 01.04.2019
money_0104=float (ads_ctr[ads_ctr['date']=='2019-04-01']['money'])
view_0104=float (ads_ctr[ads_ctr['date']=='2019-04-01']['event_x'])
clicks_0104=float (ads_ctr[ads_ctr['date']=='2019-04-01']['event_y'])
ctr_0104=float (ads_ctr[ads_ctr['date']=='2019-04-01']['CTR'])

# Разница в процентах
diff_money= round((money_0204 - money_0104)/money_0104*100)
diff_view= round ((view_0204 - view_0104)/view_0104*100)
diff_clicks= round((clicks_0204 - clicks_0104)/clicks_0104*100)
diff_ctr= round((ctr_0204 - ctr_0104)/ctr_0104*100)
print ('Метрики посчитаны')


massage_vk= f'''Отчет по объявлению 121288 за 2 апреля\n
Траты: {money_0204} ({diff_money}%)
Показы: {view_0204} ({diff_view}%)
Клики: {clicks_0204} ({diff_clicks}%)
CTR: {ctr_0204} ({diff_ctr}%)
'''
print ('Отчёт сформирован')

# Запись отчёта в текстовый файл
with open (f'report_2019-04-02.txt', 'w') as file:
    file.write(massage_vk)
print('Отчёт записан')

# Отправка отчета в ВК
app_token =''
chat_id = 1
my_id = 
vk_session = vk_api.VkApi(token=app_token)
vk = vk_session.get_api()

# DAG
vk.massages.send(chat_id=chat_id, 
                random_id=random.randint(1,2, ** 31),
                massage=massage)
print('Отчет отправлен')

