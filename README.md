Бот, в коором можно узнать текущую погоду.
Создано с помощью:

1. SQLAlchemy
2. Aiogram
3. PostgreSQL
4. API Яндекс Геокодера в связке с weatherapi.com

**Приветствие и меню:**

* При вводе команды "/start" бот приветствует пользователя и предлагает выбрать из меню:
    * "Погода в другом месте" - для запроса погоды по конкретному городу.
    * "Установить свой город" - для сохранения города проживания пользователя.
    * "Погода в моём городе" - для просмотра погоды в сохраненном городе.
    * "История" - для просмотра истории запросов.
    * 
   <a href="https://imgur.com/SY2bnEY"><img src="https://i.imgur.com/SY2bnEY.png" title="source: imgur.com" /></a>


**1. Погода в другом месте:**

* Пользователь может ввести название города, и бот покажет ему погоду в этом месте.
* Название города должно начинаться с заглавной буквы.
* Результат поиска погоды и запрос на ее получение сохраняются в базе данных бота.


**2. Установить свой город:**

* Пользователь может установить свой город проживания, и бот будет использовать его для показа погоды по умолчанию.
* Название города должно начинаться с заглавной буквы.
* Город сохраняется в базе данных бота, привязанный к Telegram ID пользователя.

   <a href="https://imgur.com/J6ZM79V"><img src="https://i.imgur.com/J6ZM79V.png" title="source: imgur.com" /></a>


**Если ввести названи города с ошибкой, или вовсе перепутать раскладку, бот всё равно всё поймёт**

   <a href="https://imgur.com/ZfpepFc"><img src="https://i.imgur.com/ZfpepFc.png" title="source: imgur.com" /></a>


**3. Погода в моём городе:**

* Если пользователь установил свой город, бот покажет ему погоду в этом городе.
* Если город не установлен, бот предложит пользователю сделать это.

   <a href="https://imgur.com/UQKSGDz"><img src="https://i.imgur.com/UQKSGDz.png" title="source: imgur.com" /></a>


**4. История:**

Пользователь может просматривать историю запросов погоды, а также удалять отдельные запросы или всю историю целиком.

   <a href="https://imgur.com/wmKelF6"><img src="https://i.imgur.com/wmKelF6.png" title="source: imgur.com" /></a>
   <a href="https://imgur.com/imwj9WW"><img src="https://i.imgur.com/imwj9WW.png" title="source: imgur.com" /></a>


**Возможности:**

* Просмотр последних запросов погоды с возможностью перелистывания страниц.
* Просмотр подробной информации о конкретном запросе погоды (дата, время, город, температура, осадки и т.д.).
* Удаление отдельного запроса из истории.
* Удаление всей истории запросов погоды.

**Как пользоваться программой:**

1. Нажмите на кнопку "История погоды" в главном меню.
2. Будет отображена первая страница с последними запросами погоды.
3. Для просмотра следующих страниц нажмите на кнопку "Далее".
4. Для просмотра подробной информации о конкретном запросе нажмите на соответствующую кнопку.
5. Для удаления отдельного запроса нажмите на кнопку "Удалить" под соответствующим запросом.
6. Для удаления всей истории нажмите на кнопку "Удалить всю историю".

**Важно:**

* Перед удалением всей истории программа запросит подтверждение.
* Удаленные запросы восстановить невозможно.
  
   <a href="https://imgur.com/sYlR3hQ"><img src="https://i.imgur.com/sYlR3hQ.png" title="source: imgur.com" /></a>
   <a href="https://imgur.com/V7gdU1Q"><img src="https://i.imgur.com/V7gdU1Q.png" title="source: imgur.com" /></a>


**Дополнительные возможности:**

* Так же у бота есть админ-панель, в которой можно смотеть данные по пользователям и истории их запросов:
  
   <a href="https://imgur.com/xIxyYcN"><img src="https://i.imgur.com/xIxyYcN.png" title="source: imgur.com" /></a>
   <a href="https://imgur.com/zYumQcB"><img src="https://i.imgur.com/zYumQcB.png" title="source: imgur.com" /></a>
   <a href="https://imgur.com/LuXYFHa"><img src="https://i.imgur.com/LuXYFHa.png" title="source: imgur.com" /></a>


**Удалять запросы из админ-панели при этом нельзя**

   <a href="https://imgur.com/uJWMywG"><img src="https://i.imgur.com/uJWMywG.png" title="source: imgur.com" /></a>


**Настройка бота:**
* Пройдёмся по настройкам бота.
  
   <a href="https://imgur.com/pQDGrqT"><img src="https://i.imgur.com/pQDGrqT.png" title="source: imgur.com" /></a>
   <a href="https://imgur.com/WfMKtlR"><img src="https://i.imgur.com/WfMKtlR.png" title="source: imgur.com" /></a>
   <a href="https://imgur.com/qVmrSkh"><img src="https://i.imgur.com/qVmrSkh.png" title="source: imgur.com" /></a>


Бот запускается командой `python app.py` из главной директории.



