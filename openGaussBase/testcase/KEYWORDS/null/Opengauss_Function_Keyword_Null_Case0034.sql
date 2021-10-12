--  @testpoint:opengauss关键字null(保留)，作为游标名

--前置条件
drop table if exists null_test cascade;
create table null_test(cid int,fid int);

--关键字不带引号-失败
start transaction;
cursor null for select * from null_test order by 1;
close null;
end;

--关键字带双引号-成功
start transaction;
cursor "null" for select * from null_test order by 1;
close "null";
end;

--关键字带单引号-合理报错
start transaction;
cursor 'null' for select * from null_test order by 1;
close 'null';
end;

--关键字带反引号-合理报错
start transaction;
cursor `null` for select * from null_test order by 1;
close `null`;
end;

--清理环境
drop table null_test cascade;