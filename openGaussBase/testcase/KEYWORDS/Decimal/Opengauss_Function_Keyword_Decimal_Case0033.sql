--  @testpoint:opengauss关键字decimal(非保留)，作为视图名


--关键字decimal作为视图名，不带引号，创建成功
CREATE or replace VIEW decimal AS
SELECT * FROM pg_tablespace WHERE spcname = 'pg_default';
drop view decimal;

--关键字decimal作为视图名，加双引号，创建成功
CREATE  or replace VIEW "decimal" AS
SELECT * FROM pg_tablespace WHERE spcname = 'pg_default';
drop VIEW "decimal";

--关键字decimal作为视图名，加单引号，合理报错
CREATE or replace VIEW 'decimal' AS
SELECT * FROM pg_tablespace WHERE spcname = 'pg_default';

--关键字decimal作为视图名，加反引号，合理报错
CREATE or replace VIEW `decimal` AS
SELECT * FROM pg_tablespace WHERE spcname = 'pg_default';

