--  @testpoint:opengauss关键字equals(非保留)，作为用户名

--关键字equals作为用户名不带引号，创建成功
drop user if exists equals;
CREATE USER equals PASSWORD 'Bigdata@123';
drop user equals;

--关键字equals作为用户名加双引号，创建成功
drop user if exists "equals";
CREATE USER "equals" PASSWORD 'Bigdata@123';
drop user "equals";
 
--关键字equals作为用户名加单引号，合理报错
CREATE USER 'equals' PASSWORD 'Bigdata@123';

--关键字equals作为用户名加反引号，合理报错
CREATE USER `equals` PASSWORD 'Bigdata@123';
