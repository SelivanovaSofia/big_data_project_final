# Итоговый курсовой проект по предмету: Наука о данных и аналитика больших объемов информации

**Члены рабочей группы**

* Меркадо Оудалова Данило, гр. 3540904/20202
* Селиванова Софья Алексеевна, гр. 3540904/20202
* Козлов Денис Олегович, гр. 3540904/20202
* Гармаева Екатерина Ринчиновна, гр. 3743801/12601
* Маслова Элла, гр. 3743801/12601

## 1. Введение
![https://www.renaissancecapital.com/logos/CIAN_logo.jpg](https://www.renaissancecapital.com/logos/CIAN_logo.jpg)

> Рынок аренды жилой недвижимости в России не до конца сформирован, кроме того, в этой сфере существуют проблемы в развитии арендных отношений, препятствующие формированию их устойчивой системы. Расширение сферы аренды жилой недвижимости необходимо для обеспечения экономической стабильности в стране и развития рынка аренды жилья.

Актуальность этого проекта обусловлена тем, что мы можем определить текущее состояние рынка недвижимости в основных регионах России с помощью анализа на сайте [cian.ru](cian.ru)

**Реализованные модули**

* Модуль синтаксического анализа и доставки данных в Kafka
* Модуль Кафки и Zookeeper
* Модуль очистки данных и сохранения в MongoDB
* Я создаю модуль MongoDB и реплицирую MongoDB
* Модуль Monstache
* Модуль эластичного поиска с помощью Kibana
![https://github.com/SelivanovaSofia/big_data_project_final/blob/main/scheme_project.png](https://github.com/SelivanovaSofia/big_data_project_final/blob/main/scheme_project.png)

## 2. Основные требования для использования разработанных модулей


Ниже приведены основные требования, хотя проект может работать с меньшим количеством ресурсов, это не рекомендуется из-за большого объема хранимых данных.

* Docker
* Docker compose
* Python 3.10
* Оперативная ПАМЯТЬ >= 12 ГБ
* Память >= 50 ГБ
* Количество ядер процессора >=4

## 3. Шаги по запуску программы

### _Клонировать репозиторий_
`git clone https://github.com/SelivanovaSofia/big_data_project_final`

### _Zookeper - Kafka_
Войти в папку `big_data_project_final/zookeper-kafka`
Изменить файлdocker-compose.yml

(Необходимо указать IP-адрес в случае использования на внешнем сервере, открыть нужные порты и дополнительные настройки)

### _MongoDB, MongoDB Replica и Monstache_

Также можно использовать ENV изменить учетные данные и начать выполнять следующие шаги с этого шага.

Войти в папку `big_data_project_final/mongo-monstache`

#### Для запуска кластера:
```
docker-compose up
```

#### Подключение к основному узлу
```
docker-compose exec tut12-mongo-primary mongo -u "root" -p "password"
```

#### Создайте экземпляр набора реплик
```
rs.initiate({"_id" : "tut12-replica-set","members" : [{"_id" : 0,"host" : "tut12-mongo-primary:27017"},{"_id" : 1,"host" : "tut12-mongo-worker-1:27017"},{"_id" : 2,"host" : "tut12-mongo-worker-2:27017"},{"_id" : 3,"host" : "tut12-mongo-worker-3:27017"}]});
```

#### Установите приоритет ведущего по сравнению с другими узлами
```
conf = rs.config();
conf.members[0].priority = 2;
rs.reconfig(conf);
```

#### Создайте администратора кластера
```
use admin;
db.createUser({user: "cluster_admin",pwd: "password",roles: [ { role: "userAdminAnyDatabase", db: "admin" },  { "role" : "clusterAdmin", "db" : "admin" } ]});
db.auth("cluster_admin", "password");
```

#### Создайте коллекцию в базе данных
```
use my_data;
db.createUser({user: "my_user",pwd: "password",roles: [ { role: "readWrite", db: "my_data" } ]});
db.createCollection('my_collection');
```

#### Проверка учетных данных
```
docker-compose exec tut12-mongo-primary mongo -u "my_user" -p "password" --authenticationDatabase "my_data"
```


#### Monstache (Golang)
Модифицируйте учетные данные и доступ к эластичному поиску.

### _Elastic Search и Kibana_

Необходимо изменить только учетные данные в файле docker-compose. yml

### _Python Parser_

> Для синтаксического анализатора python необходимо создать образ docker из Dockerfile, после этого нужно только запустить docker run с помощью "имя образа"
> 
> Этот модуль в значительной степени автоматизирован. Он содержит crontab, то есть автоматизированную задачу для выполнения синтаксического анализа данных веб-страницы [cian.ru](cian.ru)
> 
> Необходимо изменить учетные данные, а также IP-адрес, на котором вы хотите запустить проект.

### _Python Consumer_

В случае с нашим Python Consumer он не на 100% автоматизирован, учетные данные необходимо менять по мере необходимости. В дополнение к изменению темы, которую вы хотите получить и которая выполняет полный конвейер



