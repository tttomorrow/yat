--  @testpoint:opengauss关键字nullif(非保留)，作为视图名


--关键字explain作为视图名，不带引号，创建成功
CREATE or replace VIEW nullif AS
SELECT * FROM pg_tablespace WHERE spcname = 'pg_default';
drop view nullif;

--关键字explain作为视图名，加双引号，创建成功
CREATE  or replace VIEW "nullif" AS
SELECT * FROM pg_tablespace WHERE spcname = 'pg_default';
drop VIEW "nullif";

--关键字explain作为视图名，加单引号，合理报错
CREATE or replace VIEW 'nullif' AS
SELECT * FROM pg_tablespace WHERE spcname = 'pg_default';

--关键字explain作为视图名，加反引号，合理报错
CREATE or replace VIEW `nullif` AS
SELECT * FROM pg_tablespace WHERE spcname = 'pg_default';

