--  @testpoint:opengauss关键字restrict(非保留)，作为视图名


--关键字restrict作为视图名，不带引号，创建成功
CREATE or replace VIEW restrict AS
SELECT * FROM pg_tablespace WHERE spcname = 'pg_default';
drop view restrict;

--关键字restrict作为视图名，加双引号，创建成功
CREATE  or replace VIEW "restrict" AS
SELECT * FROM pg_tablespace WHERE spcname = 'pg_default';
drop VIEW "restrict";

--关键字restrict作为视图名，加单引号，合理报错
CREATE or replace VIEW 'restrict' AS
SELECT * FROM pg_tablespace WHERE spcname = 'pg_default';

--关键字restrict作为视图名，加反引号，合理报错
CREATE or replace VIEW `restrict` AS
SELECT * FROM pg_tablespace WHERE spcname = 'pg_default';

