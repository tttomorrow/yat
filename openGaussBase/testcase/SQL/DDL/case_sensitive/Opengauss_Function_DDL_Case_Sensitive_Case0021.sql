--  @testpoint: --alter验证字段大小写敏感
alter table false_1 modify B int;
alter table false_1 modify b int;

SELECT col_description(a.attrelid,a.attnum) as comment,format_type(a.atttypid,a.atttypmod) as type,a.attname as name, a.attnotnull as notnull
FROM pg_class as c,pg_attribute as a
where c.relname = 'false_1' and a.attrelid = c.oid and a.attnum>0;