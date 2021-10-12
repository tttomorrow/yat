--  @testpoint:opengauss关键字cursor_name(非保留)，作为用户名

--关键字cursor_name作为用户名不带引号，创建成功
drop user if exists cursor_name;
CREATE USER cursor_name PASSWORD 'Bigdata@123';
drop user cursor_name;

--关键字cursor_name作为用户名加双引号，创建成功
drop user if exists "cursor_name";
CREATE USER "cursor_name" PASSWORD 'Bigdata@123';
drop user "cursor_name";
 
--关键字cursor_name作为用户名加单引号，合理报错
CREATE USER 'cursor_name' PASSWORD 'Bigdata@123';

--关键字cursor_name作为用户名加反引号，合理报错
CREATE USER `cursor_name` PASSWORD 'Bigdata@123';
