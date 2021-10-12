--  @testpoint:opengauss关键字range(非保留)，作为用户名

--关键字range作为用户名不带引号，创建成功
drop user if exists range;
CREATE USER range PASSWORD 'Bigdata@123';
drop user range;

--关键字range作为用户名加双引号，创建成功
drop user if exists "range";
CREATE USER "range" PASSWORD 'Bigdata@123';
drop user "range";
 
--关键字range作为用户名加单引号，合理报错
CREATE USER 'range' PASSWORD 'Bigdata@123';

--关键字range作为用户名加反引号，合理报错
CREATE USER `range` PASSWORD 'Bigdata@123';
