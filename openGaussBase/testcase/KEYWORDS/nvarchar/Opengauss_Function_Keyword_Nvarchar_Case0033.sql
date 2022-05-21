-- @testpoint: opengauss关键字nvarchar(非保留)，作为视图名 部分测试点合理报错


--step1:关键字explain作为视图名，不带引号;expect:创建成功
create or replace view nvarchar as
select * from pg_tablespace where spcname = 'pg_default';
drop view nvarchar;

--step2:关键字explain作为视图名，加双引号;expect:创建成功
create  or replace view "nvarchar" AS
Select * from pg_tablespace where spcname = 'pg_default';
drop view "nvarchar";

--step3:关键字explain作为视图名，加单引号;expect:合理报错
create or replace view 'nvarchar' as
select * from pg_tablespace where spcname = 'pg_default';

--step4:关键字explain作为视图名，加反引号;expect:合理报错
create or replace view `nvarchar` as
select * from pg_tablespace where spcname = 'pg_default';

