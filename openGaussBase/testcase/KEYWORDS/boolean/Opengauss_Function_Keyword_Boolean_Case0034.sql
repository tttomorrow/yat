--  @testpoint:opengauss关键字boolean(非保留)，作为游标名
--前置条件
drop table if exists boolean_test cascade;
create table boolean_test(cid int,fid int);

--关键字不带引号-成功
start transaction;
cursor boolean for select * from boolean_test order by 1;
close boolean;
end;

--关键字带双引号-成功
start transaction;
cursor "boolean" for select * from boolean_test order by 1;
close "boolean";
end;

--关键字带单引号-合理报错
start transaction;
cursor 'boolean' for select * from boolean_test order by 1;
close 'boolean';
end;

--关键字带反引号-合理报错
start transaction;
cursor `boolean` for select * from boolean_test order by 1;
close `boolean`;
end;

--清理环境
drop table boolean_test;