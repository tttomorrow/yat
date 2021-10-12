--  @testpoint:opengauss关键字destructor(非保留)，作为视图名


--关键字destructor作为视图名，不带引号，创建成功
CREATE or replace VIEW destructor AS
SELECT * FROM pg_tablespace WHERE spcname = 'pg_default';
drop view destructor;

--关键字destructor作为视图名，加双引号，创建成功
CREATE  or replace VIEW "destructor" AS
SELECT * FROM pg_tablespace WHERE spcname = 'pg_default';
drop VIEW "destructor";

--关键字destructor作为视图名，加单引号，合理报错
CREATE or replace VIEW 'destructor' AS
SELECT * FROM pg_tablespace WHERE spcname = 'pg_default';

--关键字destructor作为视图名，加反引号，合理报错
CREATE or replace VIEW `destructor` AS
SELECT * FROM pg_tablespace WHERE spcname = 'pg_default';

