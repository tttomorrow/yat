--  @testpoint:opengauss关键字begin_non_anoyblock(非保留)，作为用户名
--关键字begin_non_anoyblock作为用户名不带引号，创建成功
drop user if exists begin_non_anoyblock;
CREATE USER begin_non_anoyblock PASSWORD 'Bigdata@123';

--清理环境
drop user begin_non_anoyblock;

--关键字begin_non_anoyblock作为用户名加双引号，创建成功
drop user if exists "begin_non_anoyblock";
CREATE USER "begin_non_anoyblock" PASSWORD 'Bigdata@123';

--清理环境
drop user "begin_non_anoyblock";

--关键字begin_non_anoyblock作为用户名加单引号，合理报错
CREATE USER 'begin_non_anoyblock' PASSWORD 'Bigdata@123';

--关键字begin_non_anoyblock作为用户名加反引号，合理报错
CREATE USER `begin_non_anoyblock` PASSWORD 'Bigdata@123';
