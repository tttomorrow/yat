-- @testpoint: 创建临时表，使用序列类型，合理报错
-- @modify at: 2020-11-24
--建表
drop table if exists temp_table_066;
create temporary table temp_table_066
(
    id    serial,
    name  text
);
--创建序列，并通过nextval('sequence_name')函数指定为某一字段的默认值
drop sequence if exists sequence_066 cascade;
create sequence sequence_066 cache 100;
--建表
drop table if exists temp_table_066_bak;
create temporary table temp_table_066_bak
(
    id   int not null default nextval('sequence_066'),
    name text
);
--插入数据
insert into temp_table_066_bak values(1,'2');
insert into temp_table_066_bak  (name) values('3');
insert into temp_table_066_bak (name) values('6');
--查询表
select * from temp_table_066_bak;
--删表
drop table temp_table_066_bak;
--删除序列
drop sequence if exists sequence_066 cascade;
