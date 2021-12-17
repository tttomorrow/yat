--  @testpoint: clob:隐式转换支持clob转为number:转换为number的原数据不由数字组成:合理报错
--建表
drop table if exists test_clob_22 CASCADE;
create table test_clob_22(id int,name1 number);

--插入数据
insert into test_clob_22 VALUES(1,cast('a1234567890' as CLOB));

--查询字段信息
SELECT format_type(a.atttypid,a.atttypmod) as type
FROM pg_class as c,pg_attribute as a
where c.relname = 'test_clob_22' and a.attrelid = c.oid and a.attnum>0;

--清理数据
drop table if exists test_clob_22 CASCADE;