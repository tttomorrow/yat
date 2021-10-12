--  @testpoint:opengauss关键字direct(非保留)，作为用户名

--关键字direct作为用户名不带引号，创建成功
drop user if exists direct;
CREATE USER direct PASSWORD 'Bigdata@123';
drop user direct;

--关键字direct作为用户名加双引号，创建成功
drop user if exists "direct";
CREATE USER "direct" PASSWORD 'Bigdata@123';
drop user "direct";
 
--关键字direct作为用户名加单引号，合理报错
CREATE USER 'direct' PASSWORD 'Bigdata@123';

--关键字direct作为用户名加反引号，合理报错
CREATE USER `direct` PASSWORD 'Bigdata@123';
