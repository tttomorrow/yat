--  @testpoint:opengauss关键字checkpoint(非保留)，作为视图名
--关键字checkpoint作为视图名，不带引号，创建成功
CREATE or replace VIEW checkpoint AS
SELECT * FROM pg_tablespace WHERE spcname = 'pg_default';

--清理环境
drop view checkpoint;

--关键字checkpoint作为视图名，加双引号，创建成功
CREATE  or replace VIEW "checkpoint" AS
SELECT * FROM pg_tablespace WHERE spcname = 'pg_default';

--清理环境
drop VIEW "checkpoint";

--关键字checkpoint作为视图名，加单引号，合理报错
CREATE or replace VIEW 'checkpoint' AS
SELECT * FROM pg_tablespace WHERE spcname = 'pg_default';

--关键字checkpoint作为视图名，加反引号，合理报错
CREATE or replace VIEW `checkpoint` AS
SELECT * FROM pg_tablespace WHERE spcname = 'pg_default';
