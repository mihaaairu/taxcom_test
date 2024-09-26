-- Ознакомимся с содержимым
SELECT * FROM clients
SELECT * FROM managers
SELECT * FROM invoices ORDER BY (date_created, invoice_number) DESC


-- Выборка последних 20 счетов с сортировкой по дате и номеру счета в дате
SELECT * FROM invoices ORDER BY (date_created, invoice_number)  DESC LIMIT 20;

-- Выборки за последнюю неделю, месяц, год с сортировкой по дате и номеру счета в дате
SELECT * FROM invoices WHERE date_created >= NOW() - INTERVAL '7 days' ORDER BY (date_created, invoice_number) DESC;
SELECT * FROM invoices WHERE date_created >= NOW() - INTERVAL '30 days' ORDER BY (date_created, invoice_number) DESC;
SELECT * FROM invoices WHERE date_created >= NOW() - INTERVAL '365 days' ORDER BY (date_created, invoice_number) DESC;

-- Выборка счетов по контрагенту
SELECT * FROM invoices WHERE client_id = 'b3d4f870-c142-4f3c-963d-ef00f3f25aa1' ORDER BY (date_created, invoice_number) DESC

-- Выборка счетов по номеру счета в дате
SELECT * FROM invoices WHERE invoice_number = 1 ORDER BY (date_created, invoice_number) DESC
