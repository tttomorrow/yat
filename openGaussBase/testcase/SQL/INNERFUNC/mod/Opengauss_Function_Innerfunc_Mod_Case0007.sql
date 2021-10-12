-- @testpoint: mod函数用于条件表达式case when
select case when 2>232 then mod('434234',454) else mod('434',454) end from sys_dummy;
select case when 2>1 then mod('434234',454) else 323 end from sys_dummy;
select case when 2>232 then 323  else mod('434234',454) end from sys_dummy;