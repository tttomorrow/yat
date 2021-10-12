--  @testpoint:opengauss关键字column_name(非保留)，作为用户名

--关键字column_name作为用户名不带引号，创建成功
drop user if exists column_name;
CREATE USER column_name PASSWORD 'Bigdata@123';
drop user column_name;

--关键字column_name作为用户名加双引号，创建成功
drop user if exists "column_name";
CREATE USER "column_name" PASSWORD 'Bigdata@123';
drop user "column_name";
 
--关键字column_name作为用户名加单引号，合理报错
CREATE USER 'column_name' PASSWORD 'Bigdata@123';

--关键字column_name作为用户名加反引号，合理报错
CREATE USER `column_name` PASSWORD 'Bigdata@123';
