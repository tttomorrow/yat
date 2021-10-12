--  @testpoint:openGauss保留关键字then作为视图名

--不带引号，合理报错
CREATE or replace VIEW then AS
SELECT * FROM pg_tablespace WHERE spcname = 'pg_default';

--openGauss保留关键字then作为视图名，加双引号，创建成功
CREATE  or replace VIEW "then" AS
SELECT * FROM pg_tablespace WHERE spcname = 'pg_default';
drop VIEW "then";

--openGauss保留关键字then作为视图名，加单引号，合理报错
CREATE or replace VIEW 'then' AS
SELECT * FROM pg_tablespace WHERE spcname = 'pg_default';

--openGauss保留关键字then作为视图名，加反引号，合理报错
CREATE or replace VIEW `then` AS
SELECT * FROM pg_tablespace WHERE spcname = 'pg_default';