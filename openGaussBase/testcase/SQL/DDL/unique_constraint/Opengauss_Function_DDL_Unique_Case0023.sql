-- @testpoint: 使用alter...drop删除约束，语法错误，合理报错
-- @modify at: 2020-11-23
--drop语法错误
drop table if exists test_unique_constraint023;
create table test_unique_constraint023 (id_p int not null, lastname varchar(255) not null,firstname varchar(255), address varchar(255), city varchar(255),constraint uc_personid unique (id_p));
--删除约束，报错
alter table test_unique_constraint023 drop uc_personid;
--查询约束名，依然存在
select conname,contype from pg_constraint where conrelid = (select oid from pg_class where relname = 'test_unique_constraint023');
--删表
drop table if exists test_unique_constraint023;
