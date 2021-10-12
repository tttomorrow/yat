-- @testpoint: 插入非法字符,合理报错

drop table if exists test_uuid_09;
create table test_uuid_09 (id uuid);
insert into test_uuid_09 values ('……（*（%……&');
drop table test_uuid_09;