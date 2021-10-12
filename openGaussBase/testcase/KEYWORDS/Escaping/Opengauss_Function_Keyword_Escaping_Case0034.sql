-- @testpoint: opengauss关键字escaping(非保留)，作为游标名，部分测试点合理报错

--前置条件
drop table if exists escaping_test cascade;
create table escaping_test(cid int,fid int);

--关键字不带引号-成功
start transaction;
cursor escaping for select * from escaping_test order by 1;
close escaping;
end;

--关键字带双引号-成功
start transaction;
cursor "escaping" for select * from escaping_test order by 1;
close "escaping";
end;

--关键字带单引号-合理报错
start transaction;
cursor 'escaping' for select * from escaping_test order by 1;
close 'escaping';
end;

--关键字带反引号-合理报错
start transaction;
cursor `escaping` for select * from escaping_test order by 1;
close `escaping`;
end;
drop table if exists escaping_test cascade;
