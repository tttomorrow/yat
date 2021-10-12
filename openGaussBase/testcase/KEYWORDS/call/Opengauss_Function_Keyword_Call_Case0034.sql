--  @testpoint:opengauss关键字call(非保留)，作为游标名
--前置条件
drop table if exists call_test cascade;
create table call_test(cid int,fid int);

--关键字不带引号-成功
start transaction;
cursor call for select * from call_test order by 1;
close call;
end;

--关键字带双引号-成功
start transaction;
cursor "call" for select * from call_test order by 1;
close "call";
end;

--关键字带单引号-合理报错
start transaction;
cursor 'call' for select * from call_test order by 1;
close 'call';
end;

--关键字带反引号-合理报错
start transaction;
cursor `call` for select * from call_test order by 1;
close `call`;
end;

--清理环境
drop table call_test;