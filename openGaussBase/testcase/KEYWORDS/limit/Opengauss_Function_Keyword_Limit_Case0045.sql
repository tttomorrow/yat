-- @testpoint: 使用关键字limit为列名的普通表创建视图
drop table if exists test_limit_007h CASCADE;
create table test_limit_007h ("LIMIT" int);
insert into test_limit_007h values (1);

create or replace view v_limit_001 as select "LIMIT" from test_limit_007h;
select "LIMIT" from v_limit_001 order by "LIMIT";
--清理环境
drop table if exists test_limit_007h cascade;