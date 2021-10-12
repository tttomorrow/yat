--  @testpoint:opengauss关键字referencing(非保留)，作为用户名

--关键字referencing作为用户名不带引号，创建成功
drop user if exists referencing;
CREATE USER referencing PASSWORD 'Bigdata@123';
drop user referencing;

--关键字referencing作为用户名加双引号，创建成功
drop user if exists "referencing";
CREATE USER "referencing" PASSWORD 'Bigdata@123';
drop user "referencing";
 
--关键字referencing作为用户名加单引号，合理报错
CREATE USER 'referencing' PASSWORD 'Bigdata@123';

--关键字referencing作为用户名加反引号，合理报错
CREATE USER `referencing` PASSWORD 'Bigdata@123';
