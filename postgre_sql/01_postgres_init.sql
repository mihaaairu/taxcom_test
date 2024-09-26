-- Создание таблицы менеджеров
CREATE TABLE IF NOT EXISTS managers(
    id uuid PRIMARY KEY,  -- Уникальный идентификатор менеджера (первичный ключ)
    "name" varchar(50) NOT NULL  -- Имя менеджера
);

-- Создание таблицы контрагентов
CREATE TABLE IF NOT EXISTS clients(
    id uuid PRIMARY KEY,  -- Уникальный идентификатор контрагента (первичный ключ)
    "name" varchar(50) NOT NULL  -- Имя/название контрагента
);


-- Вспомогательная таблица для сохранения последнего invoice_number в дате.
CREATE TABLE IF NOT EXISTS invoice_number_tracker (
    date_created DATE PRIMARY KEY,
    last_invoice_number INT NOT NULL
);


----------------------------------------------------------
----------------------------------------------------------
-- Создание таблицы счетов
CREATE TABLE IF NOT EXISTS invoices(
	invoice_id uuid PRIMARY KEY,  -- Уникальный идентификатор счета (первичный ключ)
	invoice_number int NOT NULL,  -- Номер счёта
	manager_id uuid NOT NULL,  -- Уникальный идентификатор менеджера (внешний ключ к таблице managers)
	client_id uuid NOT NULL,  -- Уникальный идентификатор контрагента (внешний ключ к таблице clients)
	date_created date NOT NULL,  -- Дата создания счёта
	amount NUMERIC(20, 2) NOT NULL,  -- Сумма на счёте
	payment_status varchar(50) NOT NULL,  -- Статус платежа (не оплачен/оплачен/оплачен частично/отменен)
	shipment_status varchar(50) NOT NULL,  -- Статус отгрузки (не отгружен/отгружен частично/отгружен)

    -- Связь с таблицей менеджеров
    FOREIGN KEY (manager_id) REFERENCES managers(id)
        ON DELETE SET NULL  -- Установить NULL в случае удаления менеджера из таблицы managers
        ON UPDATE CASCADE,  -- Обновить значение ключа в случае обновления manager_id в таблице managers

    -- Связь с таблицей контрагентов
    FOREIGN KEY (client_id) REFERENCES clients(id)
        ON DELETE SET NULL  -- Установить NULL в случае удаления клиента из таблицы clients
        ON UPDATE CASCADE  -- Обновить значение ключа в случае обновления client_id в таблице clients
);

-- Индексы для поиска по деталям счета (номер счета, статус платежа, статус отгрузки)
CREATE INDEX idx_invoice_number ON invoices (invoice_number);
CREATE INDEX idx_payment_status ON invoices (payment_status);
CREATE INDEX idx_shipment_status ON invoices (shipment_status);
-- Индекс для выборки за определенную дату или за неделю/месяц/год
CREATE INDEX idx_invoices_date_created ON invoices (date_created);
-- Индексы для поиска по лицам (менеджер/контрагент)
CREATE INDEX idx_manager_id ON invoices (manager_id);
CREATE INDEX idx_client_id ON invoices (client_id);

----------------------------------------------------------
-- Сахар для работы с invoice_number.
-- Возможно overhead и будет тормозить систему на highload прогонах, но с функциональной точки зрения соответствует ТЗ.
-- В ТЗ сказано, что нумерация может начинаться заново при переходе на новую дату.
-- Здесь реализован пример с обновлением нумерации каждые сутки.
-- Каждый день invoice_number будет инкрементироваться с 1.
-- Изменение даты в записи обновляет invoice_number аналогично поведению типа данных serial.



-- Функция для триггера, назначает invoice_number для новой записи.
CREATE OR REPLACE FUNCTION update_invoice_number()
RETURNS TRIGGER AS $$
DECLARE
    _last_invoice_number INT;
BEGIN
    -- Проверяем на вхождение новой даты в существующие.
    SELECT last_invoice_number INTO _last_invoice_number
    FROM invoice_number_tracker
    WHERE date_created = NEW.date_created;

    -- Если дата новая, создаем для нее invoice_number_счетчик и назначаем invoice_number в новой записи.
    IF NOT FOUND THEN
        NEW.invoice_number := 1;
        INSERT INTO invoice_number_tracker (date_created, last_invoice_number)
        VALUES (NEW.date_created, NEW.invoice_number);

    -- Если дата уже существует, инкрементируем ее счетчик и назначаем invoice_number для новой записи.
    ELSE
        NEW.invoice_number := _last_invoice_number + 1;
        UPDATE invoice_number_tracker
        SET last_invoice_number = NEW.invoice_number
        WHERE date_created = NEW.date_created;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Создаем триггер для вызова функции update_invoice_number при любом действии с датой (создание новой записи, обновление даты в записи).
-- При удалении записи, новая запись также получит инкрементированный номер.
-- Логика сделана с упором на то, что любое изменение в базе данных должно быть отображено, пусть даже и минималистично, в виде обновления invoice_number.
-- Любое перемещение записей по датам будет расцениваться как создание новой записи.
CREATE TRIGGER invoice_number_trigger
BEFORE INSERT OR UPDATE OF date_created ON invoices
FOR EACH ROW EXECUTE FUNCTION update_invoice_number();

