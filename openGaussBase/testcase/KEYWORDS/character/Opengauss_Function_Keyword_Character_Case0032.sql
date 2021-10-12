--  @testpoint:opengauss关键字character(非保留)，作为用户名
--关键字character作为用户名不带引号，创建成功
drop user if exists character;
CREATE USER character PASSWORD 'Bigdata@123';

--清理环境
drop user character;

--关键字character作为用户名加双引号，创建成功
drop user if exists "character";
CREATE USER "character" PASSWORD 'Bigdata@123';

--清理环境
drop user "character";

--关键字character作为用户名加单引号，合理报错
CREATE USER 'character' PASSWORD 'Bigdata@123';

--关键字character作为用户名加反引号，合理报错
CREATE USER `character` PASSWORD 'Bigdata@123';
