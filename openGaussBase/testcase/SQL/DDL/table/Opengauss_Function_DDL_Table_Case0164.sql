-- @testpoint: 创建列存表以及列存表GIN索引
drop table if exists table_t3;
create table table_t3(a int, b text) with (orientation = column);
DROP INDEX if exists gin_test;
create index gin_test on table_t3 using gin(to_tsvector('ngram', b));
DROP INDEX if exists gin_test;
drop table if exists table_t3;