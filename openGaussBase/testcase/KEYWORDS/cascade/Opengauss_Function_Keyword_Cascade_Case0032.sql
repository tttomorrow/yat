--  @testpoint:opengauss关键字cascade(非保留)，作为用户名
--关键字cascade作为用户名不带引号，创建成功
drop user if exists cascade;
CREATE USER cascade PASSWORD 'Bigdata@123';

--清理环境
drop user cascade;

--关键字cascade作为用户名加双引号，创建成功
drop user if exists "cascade";
CREATE USER "cascade" PASSWORD 'Bigdata@123';

--清理环境
drop user "cascade";

--关键字cascade作为用户名加单引号，合理报错
CREATE USER 'cascade' PASSWORD 'Bigdata@123';

--关键字cascade作为用户名加反引号，合理报错
CREATE USER `cascade` PASSWORD 'Bigdata@123';
