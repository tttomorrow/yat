--  @testpoint:opengauss关键字ada(非保留)，作为游标名
--前置条件
drop table if exists ada_test cascade;
create table ada_test(cid int,fid int);

--关键字不带引号-成功
start transaction;
cursor ada for select * from ada_test order by 1;
close ada;
end;

--关键字带双引号-成功
start transaction;
cursor "ada" for select * from ada_test order by 1;
close "ada";
end;

--关键字带单引号-合理报错
start transaction;
cursor 'ada' for select * from ada_test order by 1;
close 'ada';
end;

--关键字带反引号-合理报错
start transaction;
cursor `ada` for select * from ada_test order by 1;
close `ada`;
end;

--清理环境
drop table ada_test;