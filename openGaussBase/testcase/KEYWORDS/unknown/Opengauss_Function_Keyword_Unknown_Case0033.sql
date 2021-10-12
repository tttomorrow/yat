--  @testpoint:opengauss关键字unknown(非保留)，作为视图名


--关键字explain作为视图名，不带引号，创建成功
CREATE or replace VIEW unknown AS
SELECT * FROM pg_tablespace WHERE spcname = 'pg_default';
drop view unknown;

--关键字explain作为视图名，加双引号，创建成功
CREATE  or replace VIEW "unknown" AS
SELECT * FROM pg_tablespace WHERE spcname = 'pg_default';
drop VIEW "unknown";

--关键字explain作为视图名，加单引号，合理报错
CREATE or replace VIEW 'unknown' AS
SELECT * FROM pg_tablespace WHERE spcname = 'pg_default';

--关键字explain作为视图名，加反引号，合理报错
CREATE or replace VIEW `unknown` AS
SELECT * FROM pg_tablespace WHERE spcname = 'pg_default';

