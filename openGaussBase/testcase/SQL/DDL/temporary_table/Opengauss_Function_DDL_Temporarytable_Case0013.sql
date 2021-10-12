-- @testpoint: 修改字段的约束，插入数据，违反约束条件，合理报错
-- @modify at: 2020-11-23
--建表
drop table if exists temp_table_alter_013;
create global temporary table temp_table_alter_013 (c1 int,ad varchar(4000) null,ad1 varchar(4000) null)on commit preserve rows;
--创建约束
alter table temp_table_alter_013 add constraint temp_table_alter_013_check check(ad in ('confirmed','unconfirmed'));
alter table temp_table_alter_013 modify ad not null;
--插入数据，报错（违反检查约束）
insert into temp_table_alter_013(ad) values (3);
--删除检查约束
alter table temp_table_alter_013 drop constraint temp_table_alter_013_check;
--插入数据，成功
insert into temp_table_alter_013(ad) values(1);
--查询表
select * from temp_table_alter_013;
--删表
drop table temp_table_alter_013;