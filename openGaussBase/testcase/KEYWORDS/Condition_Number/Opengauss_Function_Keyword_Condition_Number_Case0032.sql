--  @testpoint:opengauss关键字condition_number(非保留)，作为用户名

--关键字condition_number作为用户名不带引号，创建成功
drop user if exists condition_number;
CREATE USER condition_number PASSWORD 'Bigdata@123';
drop user condition_number;

--关键字condition_number作为用户名加双引号，创建成功
drop user if exists "condition_number";
CREATE USER "condition_number" PASSWORD 'Bigdata@123';
drop user "condition_number";
 
--关键字condition_number作为用户名加单引号，合理报错
CREATE USER 'condition_number' PASSWORD 'Bigdata@123';

--关键字condition_number作为用户名加反引号，合理报错
CREATE USER `condition_number` PASSWORD 'Bigdata@123';
