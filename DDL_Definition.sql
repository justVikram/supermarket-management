create table auth_group
(
	id int auto_increment
		primary key,
	name varchar(150) not null,
	constraint name
		unique (name)
);

create table auth_user
(
	id int auto_increment
		primary key,
	password varchar(128) not null,
	last_login datetime(6) null,
	is_superuser tinyint(1) not null,
	username varchar(150) not null,
	first_name varchar(150) not null,
	last_name varchar(150) not null,
	email varchar(254) not null,
	is_staff tinyint(1) not null,
	is_active tinyint(1) not null,
	date_joined datetime(6) not null,
	constraint username
		unique (username)
);

create table auth_user_groups
(
	id bigint auto_increment
		primary key,
	user_id int not null,
	group_id int not null,
	constraint auth_user_groups_user_id_group_id_94350c0c_uniq
		unique (user_id, group_id),
	constraint auth_user_groups_group_id_97559544_fk_auth_group_id
		foreign key (group_id) references auth_group (id),
	constraint auth_user_groups_user_id_6a12ed8b_fk_auth_user_id
		foreign key (user_id) references auth_user (id)
);

create table django_content_type
(
	id int auto_increment
		primary key,
	app_label varchar(100) not null,
	model varchar(100) not null,
	constraint django_content_type_app_label_model_76bd3d3b_uniq
		unique (app_label, model)
);

create table auth_permission
(
	id int auto_increment
		primary key,
	name varchar(255) not null,
	content_type_id int not null,
	codename varchar(100) not null,
	constraint auth_permission_content_type_id_codename_01ab375a_uniq
		unique (content_type_id, codename),
	constraint auth_permission_content_type_id_2f476e4b_fk_django_co
		foreign key (content_type_id) references django_content_type (id)
);

create table auth_group_permissions
(
	id bigint auto_increment
		primary key,
	group_id int not null,
	permission_id int not null,
	constraint auth_group_permissions_group_id_permission_id_0cd325b0_uniq
		unique (group_id, permission_id),
	constraint auth_group_permissio_permission_id_84c5c92e_fk_auth_perm
		foreign key (permission_id) references auth_permission (id),
	constraint auth_group_permissions_group_id_b120cbf9_fk_auth_group_id
		foreign key (group_id) references auth_group (id)
);

create table auth_user_user_permissions
(
	id bigint auto_increment
		primary key,
	user_id int not null,
	permission_id int not null,
	constraint auth_user_user_permissions_user_id_permission_id_14a6b632_uniq
		unique (user_id, permission_id),
	constraint auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm
		foreign key (permission_id) references auth_permission (id),
	constraint auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id
		foreign key (user_id) references auth_user (id)
);

create table django_admin_log
(
	id int auto_increment
		primary key,
	action_time datetime(6) not null,
	object_id longtext null,
	object_repr varchar(200) not null,
	action_flag smallint unsigned not null,
	change_message longtext not null,
	content_type_id int null,
	user_id int not null,
	constraint django_admin_log_content_type_id_c4bce8eb_fk_django_co
		foreign key (content_type_id) references django_content_type (id),
	constraint django_admin_log_user_id_c564eba6_fk_auth_user_id
		foreign key (user_id) references auth_user (id)
);

create table django_migrations
(
	id bigint auto_increment
		primary key,
	app varchar(255) not null,
	name varchar(255) not null,
	applied datetime(6) not null
);

create table django_session
(
	session_key varchar(40) not null
		primary key,
	session_data longtext not null,
	expire_date datetime(6) not null
);

create index django_session_expire_date_a5c62663
	on django_session (expire_date);

create table supermarketmanagement_customer
(
	customer_ph_no bigint not null
		primary key,
	first_name varchar(10) null,
	last_name varchar(10) null,
	addr_line_1 varchar(20) null,
	addr_line_2 varchar(20) null,
	id int auto_increment,
	constraint supermarketmanagement_customer_id_uindex
		unique (id)
);

create table supermarketmanagement_product
(
	product_id int not null
		primary key,
	product_name varchar(15) null,
	brand varchar(15) null,
	price int null,
	available_stock int null,
	quantity_sold int null,
	discounted_price int null,
	id int auto_increment,
	constraint supermarketmanagement_product_id_uindex
		unique (id)
);

create table supermarketmanagement_staff
(
	aadhar_no bigint not null
		primary key,
	staff_id int not null,
	first_name varchar(20) null,
	last_name varchar(20) null,
	addr_line_1 varchar(20) null,
	addr_line_2 varchar(20) null,
	job_designation varchar(10) null,
	salary int null,
	join_date date null,
	phone_no bigint null,
	id int auto_increment,
	constraint staff_staff_id_uindex
		unique (staff_id),
	constraint supermarketmanagement_staff_id_uindex
		unique (id)
);

create table supermarketmanagement_order
(
	order_id int not null
		primary key,
	order_date date null,
	customer_ph_no bigint null,
	mode_of_payment varchar(10) null,
	staff_id int null,
	id int auto_increment,
	constraint supermarketmanagement_order_id_uindex
		unique (id),
	constraint orders_customer_customer_ph_no_fk
		foreign key (customer_ph_no) references supermarketmanagement_customer (customer_ph_no)
			on update cascade on delete cascade,
	constraint orders_staff_staff_id_fk
		foreign key (staff_id) references supermarketmanagement_staff (staff_id)
			on update cascade on delete cascade
);

create table supermarketmanagement_invoice
(
	order_id int null,
	amount_paid int null,
	change_generated int null,
	id int auto_increment
		primary key,
	constraint invoice_orders_order_id_fk
		foreign key (order_id) references supermarketmanagement_order (order_id)
			on update cascade on delete cascade
);

create table supermarketmanagement_membership
(
	customer_ph_no bigint null,
	order_id int null,
	pts_added_or_redeemed int null,
	id int auto_increment
		primary key,
	constraint membership_customer_customer_ph_no_fk
		foreign key (customer_ph_no) references supermarketmanagement_customer (customer_ph_no)
			on update cascade on delete cascade,
	constraint membership_orders_order_id_fk
		foreign key (order_id) references supermarketmanagement_order (order_id)
			on update cascade on delete cascade
);

create table supermarketmanagement_ordereditems
(
	order_id int null,
	product_id int null,
	quantity int null,
	id int auto_increment
		primary key,
	constraint ordered_items_orders_order_id_fk
		foreign key (order_id) references supermarketmanagement_order (order_id)
			on update cascade on delete cascade,
	constraint ordered_items_product_product_id_fk
		foreign key (product_id) references supermarketmanagement_product (product_id)
			on update cascade on delete cascade
);

create table supermarketmanagement_salesreturn
(
	order_id int null,
	product_id int null,
	quantity int null,
	amount_to_pay int null,
	replacement_order_id int null,
	id int auto_increment
		primary key,
	constraint sales_return_orders_order_id_fk
		foreign key (order_id) references supermarketmanagement_order (order_id)
			on update cascade on delete cascade,
	constraint sales_return_orders_order_id_fk_2
		foreign key (replacement_order_id) references supermarketmanagement_order (order_id)
			on update cascade on delete cascade,
	constraint sales_return_product_product_id_fk
		foreign key (product_id) references supermarketmanagement_product (product_id)
			on update cascade on delete cascade
);

create table supermarketmanagement_supplier
(
	supplier_ph_no bigint not null
		primary key,
	agency_name varchar(20) null,
	addr_line_1 varchar(20) null,
	addr_line_2 varchar(20) null,
	id int auto_increment,
	constraint supermarketmanagement_supplier_id_uindex
		unique (id)
);

create table supermarketmanagement_procurement
(
	batch_no int not null
		primary key,
	bill_no varchar(10) null,
	amount_to_pay int null,
	supplier_ph_no bigint null,
	delivery_date date null,
	id int auto_increment,
	constraint procurement_bill_no_uindex
		unique (bill_no),
	constraint supermarketmanagement_procurement_id_uindex
		unique (id),
	constraint procurement_supplier_supplier_ph_no_fk
		foreign key (supplier_ph_no) references supermarketmanagement_supplier (supplier_ph_no)
			on update cascade on delete cascade
);

create table supermarketmanagement_procureditems
(
	batch_no int null,
	product_id int null,
	quantity int null,
	id int auto_increment
		primary key,
	constraint `procured _items_procurement_batch_no_fk`
		foreign key (batch_no) references supermarketmanagement_procurement (batch_no)
			on update cascade on delete cascade,
	constraint `procured _items_product_product_id_fk`
		foreign key (product_id) references supermarketmanagement_product (product_id)
			on update cascade on delete cascade
);

create table supermarketmanagement_purchasereturn
(
	batch_no int null,
	date date null,
	amount_returned int null,
	product_id int null,
	id int auto_increment
		primary key,
	constraint return_purchase_procurement_batch_no_fk
		foreign key (batch_no) references supermarketmanagement_procurement (batch_no)
			on update cascade on delete cascade,
	constraint return_purchase_product_product_id_fk
		foreign key (product_id) references supermarketmanagement_product (product_id)
			on update cascade on delete cascade
);

