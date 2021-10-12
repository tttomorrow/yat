--  @testpoint:opengauss关键字close(非保留)，作为用户名
--关键字close作为用户名不带引号，创建成功
drop user if exists close;
CREATE USER close PASSWORD 'Bigdata@123';

--清理环境
drop user close;

--关键字close作为用户名加双引号，创建成功
drop user if exists "close";
CREATE USER "close" PASSWORD 'Bigdata@123';

--清理环境
drop user "close";

--关键字close作为用户名加单引号，合理报错
CREATE USER 'close' PASSWORD 'Bigdata@123';

--关键字close作为用户名加反引号，合理报错
CREATE USER `close` PASSWORD 'Bigdata@123';
