-- @testpoint: unusable,设置索引不可用,验证功能正常


drop table if exists unusable_test;
create table unusable_test(id int,type varchar(10));

create index unusable_index on unusable_test(id);

alter index unusable_index unusable;

--清理环境
drop table if exists unusable_test;