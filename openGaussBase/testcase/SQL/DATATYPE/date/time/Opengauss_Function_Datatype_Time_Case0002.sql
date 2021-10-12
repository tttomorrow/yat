-- @testpoint: 输入超出上限，合理报错
-- @modified at: 2020-11-18

drop table if exists test_time02;
create table test_time02 (name time);
insert into test_time02 values ('25:00:00');
insert into test_time02 values ('23:60:00');
insert into test_time02 values ('23:23:61');
drop table test_time02;