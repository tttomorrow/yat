-- @testpoint: opengauss关键字except(保留)，作为游标名，部分测试点合理报错

--前置条件
drop table if exists except_test cascade;
create table except_test(cid int,fid int);

--关键字不带引号-失败
start transaction;
cursor except for select * from except_test order by 1;
close except;
end;

--关键字带双引号-成功
start transaction;
cursor "except" for select * from except_test order by 1;
close "except";
end;

--关键字带单引号-合理报错
start transaction;
cursor 'except' for select * from except_test order by 1;
close 'except';
end;

--关键字带反引号-合理报错
start transaction;
cursor `except` for select * from except_test order by 1;
close `except`;
end;
drop table if exists except_test cascade;
