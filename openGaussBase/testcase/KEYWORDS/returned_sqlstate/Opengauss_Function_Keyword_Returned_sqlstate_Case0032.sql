--  @testpoint:opengauss关键字returned_sqlstate(非保留)，作为用户名
--关键字returned_sqlstate作为用户名不带引号，创建成功
drop user if exists returned_sqlstate;
CREATE USER returned_sqlstate PASSWORD 'Bigdata@123';

--清理环境
drop user returned_sqlstate;

--关键字returned_sqlstate作为用户名加双引号，创建成功
drop user if exists "returned_sqlstate";
CREATE USER "returned_sqlstate" PASSWORD 'Bigdata@123';

--清理环境
drop user "returned_sqlstate";

--关键字returned_sqlstate作为用户名加单引号，合理报错
CREATE USER 'returned_sqlstate' PASSWORD 'Bigdata@123';

--关键字returned_sqlstate作为用户名加反引号，合理报错
CREATE USER `returned_sqlstate` PASSWORD 'Bigdata@123';
