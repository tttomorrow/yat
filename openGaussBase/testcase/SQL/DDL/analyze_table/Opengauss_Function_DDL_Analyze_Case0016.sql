-- @testpoint: 系统表分析

analyze  PG_CLASS ;
select * from PG_STATISTIC where starelid= (select oid from pg_class where relname='PG_CLASS');