--  @testpoint:openGauss保留关键字or作为视图名

 --不带引号-合理报错
  CREATE or replace VIEW or AS
    SELECT * FROM pg_tablespace WHERE spcname = 'pg_default';
	
 --加双引号-创建成功
    CREATE  or replace VIEW "or" AS
    SELECT * FROM pg_tablespace WHERE spcname = 'pg_default';
	
 --清理环境	
    drop VIEW "or";
	
 --加单引号-合理报错
 CREATE or replace VIEW 'or' AS
 SELECT * FROM pg_tablespace WHERE spcname = 'pg_default';
 
 --加反引号-合理报错
 CREATE or replace VIEW `or` AS
 SELECT * FROM pg_tablespace WHERE spcname = 'pg_default';