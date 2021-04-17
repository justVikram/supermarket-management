create table Branch
(
	Branch_ID int not null
		primary key,
	Branch_Name varchar(20) null,
	Location varchar(20) null
);

create table Brand
(
	Brand_ID int not null
		primary key,
	Brand_Name varchar(20) null
);

create table Customer
(
	Customer_ID int not null
		primary key,
	Customer_First_Name varchar(15) null,
	Customer_Last_Name varchar(15) null,
	Phone_Number bigint null,
	Customer_Type varchar(10) null
);

create table Job_Designation
(
	Job_ID int not null
		primary key,
	Job_Name varchar(15) null,
	Number_Of_Work_Hours int null
);

create table Payment_Info
(
	Payment_ID int not null
		primary key,
	Payment_Mode int null
);

create table Product
(
	Product_ID int not null
		primary key,
	Product_Name varchar(15) null,
	Brand_ID int null,
	Cost int not null,
	constraint Product_Brand_Brand_ID_fk
		foreign key (Brand_ID) references Brand (Brand_ID)
			on update cascade on delete cascade
);

create table Current_Inventory
(
	Product_ID int null,
	Available_Stock int null,
	Branch_ID int null,
	constraint Current_Inventory_Branch_Branch_ID_fk
		foreign key (Branch_ID) references Branch (Branch_ID)
			on update cascade on delete cascade,
	constraint Current_Inventory_Product_Product_ID_fk
		foreign key (Product_ID) references Product (Product_ID)
			on update cascade on delete cascade
);

create table Discount
(
	Product_ID int null,
	Discount_Amount int null,
	New_Price int null,
	constraint Discount_Product_Product_ID_fk
		foreign key (Product_ID) references Product (Product_ID)
			on update cascade on delete cascade
);

create table Restock_Inventory
(
	Warehouse_ID int not null
		primary key,
	Warehouse_Name varchar(20) null,
	Product_ID int null,
	Quantity int null,
	Date date null,
	constraint Restock_Inventory_Product_Product_ID_fk
		foreign key (Product_ID) references Product (Product_ID)
);

create table Staff
(
	Staff_ID int not null
		primary key,
	Job_ID int null,
	Branch_ID int null,
	Staff_First_Name varchar(15) null,
	Staff_Last_Name varchar(15) null,
	Gender varchar(1) null,
	Salary bigint null,
	constraint Staff_Branch_Branch_ID_fk
		foreign key (Branch_ID) references Branch (Branch_ID)
			on update cascade on delete cascade,
	constraint Staff_Job_Designation_Job_ID_fk
		foreign key (Job_ID) references Job_Designation (Job_ID)
			on update cascade on delete cascade
);

create table Staff_Contact_Info
(
	Staff_ID int null,
	Address_Line_1 varchar(20) null,
	Address_Line_2 varchar(20) null,
	Address_Line_3 varchar(20) null,
	Phone_Number bigint null,
	constraint Staff_Contact_Info_Staff_Staff_ID_fk
		foreign key (Staff_ID) references Staff (Staff_ID)
			on update cascade on delete cascade
);

create table Transaction
(
	Transaction_ID int not null
		primary key,
	Payment_ID int null,
	Date date null,
	Customer_ID int null,
	Staff_ID int null,
	constraint Transaction_Customer_Customer_ID_fk
		foreign key (Customer_ID) references Customer (Customer_ID),
	constraint Transaction_Payment_Info_Payment_ID_fk
		foreign key (Payment_ID) references Payment_Info (Payment_ID)
			on update cascade on delete cascade,
	constraint Transaction_Staff_Staff_ID_fk
		foreign key (Staff_ID) references Staff (Staff_ID)
);

create table Products_Sold
(
	Transaction_ID int null,
	Product_ID int null,
	constraint Products_Sold_Product_Product_ID_fk
		foreign key (Product_ID) references Product (Product_ID)
			on update cascade on delete cascade,
	constraint Products_Sold_Transaction_Transaction_ID_fk
		foreign key (Transaction_ID) references Transaction (Transaction_ID)
			on update cascade on delete cascade
);