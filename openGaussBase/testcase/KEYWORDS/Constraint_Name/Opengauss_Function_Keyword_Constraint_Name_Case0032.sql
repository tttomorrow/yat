--  @testpoint:opengauss关键字constraint_name(非保留)，作为用户名

--关键字constraint_name作为用户名不带引号，创建成功
drop user if exists constraint_name;
CREATE USER constraint_name PASSWORD 'Bigdata@123';
drop user constraint_name;

--关键字constraint_name作为用户名加双引号，创建成功
drop user if exists "constraint_name";
CREATE USER "constraint_name" PASSWORD 'Bigdata@123';
drop user "constraint_name";
 
--关键字constraint_name作为用户名加单引号，合理报错
CREATE USER 'constraint_name' PASSWORD 'Bigdata@123';

--关键字constraint_name作为用户名加反引号，合理报错
CREATE USER `constraint_name` PASSWORD 'Bigdata@123';
