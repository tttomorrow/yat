--  @testpoint:设置约束推迟时间
drop table if exists test_1;
start transaction;
create table test_1(id int  primary key DEFERRABLE INITIALLY DEFERRED ,name char(20));
insert into test_1 values(2,'Maria');
end;
drop table test_1;