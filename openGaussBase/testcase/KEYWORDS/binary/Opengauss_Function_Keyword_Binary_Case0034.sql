--  @testpoint:opengauss关键字binary(非保留)，作为游标名
--前置条件
drop table if exists binary_test cascade;
create table binary_test(cid int,fid int);

--关键字不带引号-成功
start transaction;
cursor binary for select * from binary_test order by 1;
close binary;
end;

--关键字带双引号-成功
start transaction;
cursor "binary" for select * from binary_test order by 1;
close "binary";
end;

--关键字带单引号-合理报错
start transaction;
cursor 'binary' for select * from binary_test order by 1;
close 'binary';
end;

--关键字带反引号-合理报错
start transaction;
cursor `binary` for select * from binary_test order by 1;
close `binary`;
end;

--清理环境
drop table binary_test;