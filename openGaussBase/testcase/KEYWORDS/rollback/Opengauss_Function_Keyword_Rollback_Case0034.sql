--  @testpoint:opengauss关键字rollback(非保留)，作为游标名
--前置条件
drop table if exists rollback_test cascade;
create table rollback_test(cid int,fid int);

--关键字不带引号-成功
start transaction;
cursor rollback for select * from rollback_test order by 1;
close rollback;
end;

--关键字带双引号-成功
start transaction;
cursor "rollback" for select * from rollback_test order by 1;
close "rollback";
end;

--关键字带单引号-合理报错
start transaction;
cursor 'rollback' for select * from rollback_test order by 1;
close 'rollback';
end;

--关键字带反引号-合理报错
start transaction;
cursor `rollback` for select * from rollback_test order by 1;
close `rollback`;
end;

--清理环境
drop table rollback_test;