-- @testpoint: 创建行存表以及行存表Gin索引
drop table if exists table_t3;
create table table_t3(a int, b text);
DROP INDEX if exists gin_test;
create index cgin_test on table_t3 using gin(to_tsvector('ngram', b));
DROP INDEX if exists gin_test;
drop table if exists table_t3;