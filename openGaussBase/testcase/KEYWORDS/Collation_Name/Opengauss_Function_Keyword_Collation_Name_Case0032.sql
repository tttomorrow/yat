--  @testpoint:opengauss关键字collation_name(非保留)，作为用户名

--关键字collation_name作为用户名不带引号，创建成功
drop user if exists collation_name;
CREATE USER collation_name PASSWORD 'Bigdata@123';
drop user collation_name;

--关键字collation_name作为用户名加双引号，创建成功
drop user if exists "collation_name";
CREATE USER "collation_name" PASSWORD 'Bigdata@123';
drop user "collation_name";
 
--关键字collation_name作为用户名加单引号，合理报错
CREATE USER 'collation_name' PASSWORD 'Bigdata@123';

--关键字collation_name作为用户名加反引号，合理报错
CREATE USER `collation_name` PASSWORD 'Bigdata@123';
