-- @testpoint: 查询pg_attribute系统表

--step1：当字段名为proname时，查询pg_attribute系统表; expect: 执行成功
select * from pg_attribute where attname='proname' order by attrelid asc;