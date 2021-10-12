--  @testpoint:opengauss关键字character_length(非保留)，作为用户名
--关键字character_length作为用户名不带引号，创建成功
drop user if exists character_length;
CREATE USER character_length PASSWORD 'Bigdata@123';

--清理环境
drop user character_length;

--关键字character_length作为用户名加双引号，创建成功
drop user if exists "character_length";
CREATE USER "character_length" PASSWORD 'Bigdata@123';

--清理环境
drop user "character_length";

--关键字character_length作为用户名加单引号，合理报错
CREATE USER 'character_length' PASSWORD 'Bigdata@123';

--关键字character_length作为用户名加反引号，合理报错
CREATE USER `character_length` PASSWORD 'Bigdata@123';
