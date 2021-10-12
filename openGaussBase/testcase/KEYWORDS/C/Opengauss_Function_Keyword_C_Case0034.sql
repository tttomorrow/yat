--  @testpoint:opengauss关键字c(非保留)，作为游标名
--前置条件
drop table if exists c_test cascade;
create table c_test(cid int,fid int);

--关键字不带引号-成功
start transaction;
cursor c for select * from c_test order by 1;
close c;
end;

--关键字带双引号-成功
start transaction;
cursor "c" for select * from c_test order by 1;
close "c";
end;

--关键字带单引号-合理报错
start transaction;
cursor 'c' for select * from c_test order by 1;
close 'c';
end;

--关键字带反引号-合理报错
start transaction;
cursor `c` for select * from c_test order by 1;
close `c`;
end;

--清理环境
drop table c_test;