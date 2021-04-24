--Supermarket Management System
create table customer
(
	customer_ph_no int not null
		primary key,
	first_name varchar(10) null,
	last_name varchar(10) null,
	addr_line_1 varchar(20) null,
	addr_line_2 varchar(20) null
);

create table orders
(
	order_id int not null
		primary key,
	order_date date null,
	customer_ph_no int null,
	mode_of_payment varchar(10) null,
	constraint order_customer_phone_number_fk
		foreign key (customer_ph_no) references customer (customer_ph_no)
			on update cascade on delete cascade
);

create table invoice
(
	order_id int null,
	amount_paid int null,
	change_generated int null,
	constraint invoice_orders_order_id_fk
		foreign key (order_id) references orders (order_id)
			on update cascade on delete cascade
);

create table membership
(
	customer_ph_no int null,
	order_id int null,
	pts_added_or_redeemed int null,
	constraint membership_customer_customer_ph_no_fk
		foreign key (customer_ph_no) references customer (customer_ph_no)
			on update cascade on delete cascade,
	constraint membership_orders_order_id_fk
		foreign key (order_id) references orders (order_id)
			on update cascade on delete cascade
);

create table product
(
	product_id int not null
		primary key,
	product_name varchar(15) null,
	brand varchar(15) null,
	price int null,
	available_stock int null,
	quantity_sold int null,
	discounted_price int null
);

create table ordered_items
(
	order_id int null,
	product_id int null,
	quantity int null,
	constraint ordered_items_orders_order_id_fk
		foreign key (order_id) references orders (order_id)
			on update cascade on delete cascade,
	constraint ordered_items_product_product_id_fk
		foreign key (product_id) references product (product_id)
			on update cascade on delete cascade
);

create table sales_return
(
	order_id int null,
	product_id int null,
	quantity int null,
	amount_to_pay int null,
	replacement_order_id int null,
	constraint sales_return_orders_order_id_fk
		foreign key (order_id) references orders (order_id)
			on update cascade on delete cascade,
	constraint sales_return_orders_order_id_fk_2
		foreign key (replacement_order_id) references orders (order_id)
			on update cascade on delete cascade,
	constraint sales_return_product_product_id_fk
		foreign key (product_id) references product (product_id)
			on update cascade on delete cascade
);

create table staff
(
	aadhar_number bigint not null
		primary key,
	first_name varchar(20) null,
	last_name varchar(20) null,
	phone_number int null,
	addr_line_1 varchar(20) null,
	addr_line_2 varchar(20) null,
	job_designation varchar(10) null,
	salary int null,
	join_date date null
);

create table supplier
(
	supplier_ph_no int not null
		primary key,
	agency_name varchar(20) null,
	addr_line_2 varchar(20) null,
	addr_line_1 varchar(20) null
);

create table procurement
(
	batch_no int not null
		primary key,
	bill_no varchar(10) null,
	amount_to_pay int null,
	supplier_ph_no int null,
	delivery_date int null,
	constraint procurement_bill_no_uindex
		unique (bill_no),
	constraint procurement_supplier_supplier_ph_no_fk
		foreign key (supplier_ph_no) references supplier (supplier_ph_no)
			on update cascade on delete cascade
);

create table procured_items
(
	batch_no int null,
	product_id int null,
	quantity int null,
	constraint `procured _items_procurement_batch_no_fk`
		foreign key (batch_no) references procurement (batch_no)
			on update cascade on delete cascade,
	constraint `procured _items_product_product_id_fk`
		foreign key (product_id) references product (product_id)
			on update cascade on delete cascade
);

create table purchase_return
(
	batch_no int null,
	date date null,
	amount_returned int null,
	product_id int null,
	constraint return_purchase_procurement_batch_no_fk
		foreign key (batch_no) references procurement (batch_no)
			on update cascade on delete cascade,
	constraint return_purchase_product_product_id_fk
		foreign key (product_id) references product (product_id)
			on update cascade on delete cascade
);

