--  @testpoint:opengauss关键字binary_double(非保留)，作为游标名
--前置条件
drop table if exists binary_double_test cascade;
create table binary_double_test(cid int,fid int);

--关键字不带引号-成功
start transaction;
cursor binary_double for select * from binary_double_test order by 1;
close binary_double;
end;

--关键字带双引号-成功
start transaction;
cursor "binary_double" for select * from binary_double_test order by 1;
close "binary_double";
end;

--关键字带单引号-合理报错
start transaction;
cursor 'binary_double' for select * from binary_double_test order by 1;
close 'binary_double';
end;

--关键字带反引号-合理报错
start transaction;
cursor `binary_double` for select * from binary_double_test order by 1;
close `binary_double`;
end;

--清理环境
drop table binary_double_test;