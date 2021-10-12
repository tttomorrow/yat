--  @testpoint:opengauss关键字execute(非保留)，作为视图名


--关键字execute作为视图名，不带引号，创建成功
CREATE or replace VIEW execute AS
SELECT * FROM pg_tablespace WHERE spcname = 'pg_default';
drop view execute;

--关键字execute作为视图名，加双引号，创建成功
CREATE  or replace VIEW "execute" AS
SELECT * FROM pg_tablespace WHERE spcname = 'pg_default';
drop VIEW "execute";

--关键字execute作为视图名，加单引号，合理报错
CREATE or replace VIEW 'execute' AS
SELECT * FROM pg_tablespace WHERE spcname = 'pg_default';

--关键字execute作为视图名，加反引号，合理报错
CREATE or replace VIEW `execute` AS
SELECT * FROM pg_tablespace WHERE spcname = 'pg_default';

