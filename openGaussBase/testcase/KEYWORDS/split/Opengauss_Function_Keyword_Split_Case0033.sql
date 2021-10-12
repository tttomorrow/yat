--  @testpoint:openGauss保留关键字split作为视图名

--不带引号，成功
CREATE or replace VIEW split AS
SELECT * FROM pg_tablespace WHERE spcname = 'pg_default';

--openGauss保留关键字split作为视图名，加双引号，创建成功
CREATE  or replace VIEW "split" AS
SELECT * FROM pg_tablespace WHERE spcname = 'pg_default';
drop VIEW "split";

--openGauss保留关键字split作为视图名，加单引号，合理报错
CREATE or replace VIEW 'split' AS
SELECT * FROM pg_tablespace WHERE spcname = 'pg_default';

--openGauss保留关键字split作为视图名，加反引号，合理报错
CREATE or replace VIEW `split` AS
SELECT * FROM pg_tablespace WHERE spcname = 'pg_default';