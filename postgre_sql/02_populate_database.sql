-- Предзаполнение менеджеров
INSERT INTO managers (
    id,
    "name"
) VALUES
    ('9d72f870-c142-4f3c-963d-ef00f3f25cc6', 'Jim'),
    ('5e6f1f25-c587-4ec9-bc98-25517b545432', 'Alice'),
    ('c36ef6b9-07a5-4c76-b2f7-610e1c0e60f9', 'Bob');

-- Предзаполнение контрагентов
INSERT INTO clients (
    id,
    "name"
) VALUES
    ('b3d4f870-c142-4f3c-963d-ef00f3f25aa1', 'TechCorp Inc.'),
    ('e4f1f25b-c587-4ec9-bc98-25517b545aaa', 'John Doe'),
    ('d16ef6b9-07a5-4c76-b2f7-610e1c0e60b2', 'Acme Solutions'),
    ('f8c1b903-7a7e-4f41-87b3-c3e21b78b1c4', 'Jane Smith'),
    ('12f6b3a4-6c82-4784-b17c-f0c1c6877689', 'Global Enterprises'),
    ('3c0dbb8e-d1d6-45c8-ade2-3f7933f7d9d1', 'Alice Johnson');

-- Предзаполнение счета
INSERT INTO invoices (
	invoice_id,
	manager_id,
	client_id,
	date_created,
	amount,
	payment_status,
	shipment_status
) VALUES
	('91658964-d8f7-4f01-976e-273d1c8ab080', '9d72f870-c142-4f3c-963d-ef00f3f25cc6', 'b3d4f870-c142-4f3c-963d-ef00f3f25aa1', '2024-09-26', 1000.00, 'PAID', 'NOT SHIPPED'),
	('12fe3625-8da1-490a-b17f-569d7d523bea', '9d72f870-c142-4f3c-963d-ef00f3f25cc6', 'e4f1f25b-c587-4ec9-bc98-25517b545aaa', '2024-09-11', 1500.00, 'NOT PAID', 'SHIPPED'),
	('4f19fb82-7b4d-492d-921e-f8e65a16d624', '5e6f1f25-c587-4ec9-bc98-25517b545432', 'd16ef6b9-07a5-4c76-b2f7-610e1c0e60b2', '2023-10-17', 2000.00, 'PARTIALLY PAID', 'PARTIALLY SHIPPED'),
	('c7dc5f27-8f39-4083-b353-286b4c589b20', '5e6f1f25-c587-4ec9-bc98-25517b545432', 'f8c1b903-7a7e-4f41-87b3-c3e21b78b1c4', '2024-09-26', 100.00, 'CANCELLED', 'PARTIALLY SHIPPED'),
	('9d62dc0a-88c5-49ff-a625-7a234f7fefe0', 'c36ef6b9-07a5-4c76-b2f7-610e1c0e60f9', '12f6b3a4-6c82-4784-b17c-f0c1c6877689', '2024-09-11', 150.00, 'NOT PAID', 'NOT SHIPPED'),
	('2ec9068a-1b39-42e9-acbd-de3fbe311a90', 'c36ef6b9-07a5-4c76-b2f7-610e1c0e60f9', '3c0dbb8e-d1d6-45c8-ade2-3f7933f7d9d1', '2023-10-17', 10000.00, 'PAID', 'SHIPPED');
