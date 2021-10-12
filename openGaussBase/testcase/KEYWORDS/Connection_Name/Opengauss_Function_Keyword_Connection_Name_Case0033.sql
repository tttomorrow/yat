--  @testpoint:opengauss关键字connection_name(非保留)，作为视图


--关键字connection_name作为视图名，不带引号，创建成功
CREATE or replace VIEW connection_name AS
SELECT * FROM pg_tablespace WHERE spcname = 'pg_default';

--关键字connection_name作为视图名，加双引号，创建成功
CREATE  or replace VIEW "connection_name" AS
SELECT * FROM pg_tablespace WHERE spcname = 'pg_default';
drop VIEW "connection_name";

--关键字connection_name作为视图名，加单引号，合理报错
CREATE or replace VIEW 'connection_name' AS
SELECT * FROM pg_tablespace WHERE spcname = 'pg_default';

--关键字connection_name作为视图名，加反引号，合理报错
CREATE or replace VIEW `connection_name` AS
SELECT * FROM pg_tablespace WHERE spcname = 'pg_default';

