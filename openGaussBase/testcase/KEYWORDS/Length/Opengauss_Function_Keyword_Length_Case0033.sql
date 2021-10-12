--  @testpoint:opengauss关键字Length(非保留)，作为视图名


--关键字explain作为视图名，不带引号，创建成功
CREATE or replace VIEW Length AS
SELECT * FROM pg_tablespace WHERE spcname = 'pg_default';
drop view Length;

--关键字explain作为视图名，加双引号，创建成功
CREATE  or replace VIEW "Length" AS
SELECT * FROM pg_tablespace WHERE spcname = 'pg_default';
drop VIEW "Length";

--关键字explain作为视图名，加单引号，合理报错
CREATE or replace VIEW 'Length' AS
SELECT * FROM pg_tablespace WHERE spcname = 'pg_default';

--关键字explain作为视图名，加反引号，合理报错
CREATE or replace VIEW `Length` AS
SELECT * FROM pg_tablespace WHERE spcname = 'pg_default';

