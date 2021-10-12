--  @testpoint: clob：建表作为数据类型：列存分区表：success
drop table if exists test_clob_08 cascade;
create table test_clob_08(id int,name clob)  with (orientation=column)
PARTITION BY RANGE(id)(
        PARTITION P1 VALUES LESS THAN(100),
        PARTITION P2 VALUES LESS THAN(1000),
        PARTITION P3 VALUES LESS THAN(MAXVALUE))
;
--插入数据
BEGIN
  for i in 1..10 LOOP
    insert into test_clob_08 values(i,concat('zhangsan',i));
  end LOOP;
end;
/
--查询字段信息
SELECT format_type(a.atttypid,a.atttypmod) as type
FROM pg_class as c,pg_attribute as a
where c.relname = 'test_clob_08' and a.attrelid = c.oid and a.attnum>0;
--清理数据
drop table if exists test_clob_08 CASCADE;
