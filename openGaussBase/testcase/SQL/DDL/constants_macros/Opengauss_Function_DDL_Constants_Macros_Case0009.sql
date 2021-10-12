--  @testpoint:Null有效性测试
--建表
drop table if exists test_1;
create table test_1(id int);
--插入数据null
insert into test_1 values(null);
select * from test_1;
--查询null的字节数
select char_length(null);
--给id字段创建唯一约束
alter table test_1 add constraint "id_unique" unique(id);
--插入null值，成功
insert into test_1 values(null);
--查询表的记录数（2）
select count(*) from test_1;
--查询表的记录数（非空数,0）
select count(id) from test_1;
--修改id字段为主键约束,合理报错（id列有null值）
alter table test_1 add constraint "id_primary" primary key(id);
--清空表的数据
truncate table test_1;
--修改id字段为主键约束
alter table test_1 add constraint "id_primary" primary key(id);
--插入数据null，合理报错
insert into test_1 values(null);
--删表
drop table test_1;
