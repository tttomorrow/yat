-- @testpoint: 无效值测试
drop table if exists test_boolean_001;
create table test_boolean_001 (a boolean);
insert into test_boolean_001 values(true);
insert into test_boolean_001 values(false);
commit;
drop table if exists test_boolean_001;