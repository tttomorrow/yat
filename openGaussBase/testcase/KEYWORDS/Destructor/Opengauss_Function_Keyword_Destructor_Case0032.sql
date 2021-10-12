--  @testpoint:opengauss关键字destructor(非保留)，作为用户名

--关键字destructor作为用户名不带引号，创建成功
drop user if exists destructor;
CREATE USER destructor PASSWORD 'Bigdata@123';
drop user destructor;

--关键字destructor作为用户名加双引号，创建成功
drop user if exists "destructor";
CREATE USER "destructor" PASSWORD 'Bigdata@123';
drop user "destructor";
 
--关键字destructor作为用户名加单引号，合理报错
CREATE USER 'destructor' PASSWORD 'Bigdata@123';

--关键字destructor作为用户名加反引号，合理报错
CREATE USER `destructor` PASSWORD 'Bigdata@123';
