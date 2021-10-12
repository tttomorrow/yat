-- @testpoint: 在普通表关键字limit作为列名的字段上创建索引
drop table if exists test_limit_008;
create table test_limit_008 ("LIMIT" int);
create index index_limit_001 on test_limit_008("LIMIT" );
--清理环境
drop table if exists test_limit_008;