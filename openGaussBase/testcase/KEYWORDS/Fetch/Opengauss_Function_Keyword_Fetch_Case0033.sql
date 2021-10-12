--  @testpoint:openGauss保留关键字fetch作为视图名
--openGauss保留关键字fetch作为视图名,不带引号，合理报错
  CREATE or replace VIEW fetch AS
  SELECT * FROM pg_tablespace WHERE spcname = 'pg_fetch';
 ----openGauss保留关键字fetch作为视图名，加双引号，创建成功
    CREATE  or replace VIEW "fetch" AS
    SELECT * FROM pg_tablespace WHERE spcname = 'pg_fetch';
    drop VIEW "fetch";
 ----openGauss保留关键字fetch作为视图名，加单引号，合理报错

 CREATE or replace VIEW 'fetch' AS
 SELECT * FROM pg_tablespace WHERE spcname = 'pg_fetch';
 ----openGauss保留关键字fetch作为视图名，加反引号，合理报错
 CREATE or replace VIEW `fetch` AS
 SELECT * FROM pg_tablespace WHERE spcname = 'pg_fetch';