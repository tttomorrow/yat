--  @testpoint:opengauss关键字routine(非保留)，作为游标名
--前置条件
drop table if exists routine_test cascade;
create table routine_test(cid int,fid int);

--关键字不带引号-成功
start transaction;
cursor routine for select * from routine_test order by 1;
close routine;
end;

--关键字带双引号-成功
start transaction;
cursor "routine" for select * from routine_test order by 1;
close "routine";
end;

--关键字带单引号-合理报错
start transaction;
cursor 'routine' for select * from routine_test order by 1;
close 'routine';
end;

--关键字带反引号-合理报错
start transaction;
cursor `routine` for select * from routine_test order by 1;
close `routine`;
end;

--清理环境
drop table routine_test;