--  @testpoint:opengauss关键字rebuild(非保留)，作为用户名

--关键字rebuild作为用户名不带引号，创建成功
drop user if exists rebuild;
CREATE USER rebuild PASSWORD 'Bigdata@123';
drop user rebuild;

--关键字rebuild作为用户名加双引号，创建成功
drop user if exists "rebuild";
CREATE USER "rebuild" PASSWORD 'Bigdata@123';
drop user "rebuild";
 
--关键字rebuild作为用户名加单引号，合理报错
CREATE USER 'rebuild' PASSWORD 'Bigdata@123';

--关键字rebuild作为用户名加反引号，合理报错
CREATE USER `rebuild` PASSWORD 'Bigdata@123';
