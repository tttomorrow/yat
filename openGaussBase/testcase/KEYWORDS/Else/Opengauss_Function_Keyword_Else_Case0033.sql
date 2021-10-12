--  @testpoint:openGauss保留关键字else作为视图名
--openGauss保留关键字else作为视图名,不带引号，合理报错
  CREATE or replace VIEW else AS
  SELECT * FROM pg_tablespace WHERE spcname = 'pg_else';
 ----openGauss保留关键字else作为视图名，加双引号，创建成功
    CREATE  or replace VIEW "else" AS
    SELECT * FROM pg_tablespace WHERE spcname = 'pg_else';
    drop VIEW "else";
 ----openGauss保留关键字else作为视图名，加单引号，合理报错

 CREATE or replace VIEW 'else' AS
 SELECT * FROM pg_tablespace WHERE spcname = 'pg_else';
 ----openGauss保留关键字else作为视图名，加反引号，合理报错
 CREATE or replace VIEW `else` AS
 SELECT * FROM pg_tablespace WHERE spcname = 'pg_else';