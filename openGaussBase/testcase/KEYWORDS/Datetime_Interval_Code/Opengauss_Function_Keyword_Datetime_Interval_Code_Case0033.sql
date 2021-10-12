--  @testpoint:opengauss关键字datetime_interval_code(非保留)，作为视图名


--关键字datetime_interval_code作为视图名，不带引号，创建成功
CREATE or replace VIEW datetime_interval_code AS
SELECT * FROM pg_tablespace WHERE spcname = 'pg_default';
drop view datetime_interval_code;

--关键字datetime_interval_code作为视图名，加双引号，创建成功
CREATE  or replace VIEW "datetime_interval_code" AS
SELECT * FROM pg_tablespace WHERE spcname = 'pg_default';
drop VIEW "datetime_interval_code";

--关键字datetime_interval_code作为视图名，加单引号，合理报错
CREATE or replace VIEW 'datetime_interval_code' AS
SELECT * FROM pg_tablespace WHERE spcname = 'pg_default';

--关键字datetime_interval_code作为视图名，加反引号，合理报错
CREATE or replace VIEW `datetime_interval_code` AS
SELECT * FROM pg_tablespace WHERE spcname = 'pg_default';

