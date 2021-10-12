--  @testpoint:opengauss关键字begin(非保留)，作为游标名
--前置条件
drop table if exists begin_test cascade;
create table begin_test(cid int,fid int);

--关键字不带引号-成功
start transaction;
cursor begin for select * from begin_test order by 1;
close begin;
end;

--关键字带双引号-成功
start transaction;
cursor "begin" for select * from begin_test order by 1;
close "begin";
end;

--关键字带单引号-合理报错
start transaction;
cursor 'begin' for select * from begin_test order by 1;
close 'begin';
end;

--关键字带反引号-合理报错
start transaction;
cursor `begin` for select * from begin_test order by 1;
close `begin`;
end;

--清理环境
drop table begin_test;