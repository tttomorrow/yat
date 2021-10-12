-- @testpoint: opengauss关键字constraint_name(非保留)，作为游标名，部分测试点合理报错

--前置条件
drop table if exists constraint_name_test cascade;
create table constraint_name_test(cid int,fid int);

--关键字不带引号-成功
start transaction;
cursor constraint_name for select * from constraint_name_test order by 1;
close constraint_name;
end;

--关键字带双引号-成功
start transaction;
cursor "constraint_name" for select * from constraint_name_test order by 1;
close "constraint_name";
end;

--关键字带单引号-合理报错
start transaction;
cursor 'constraint_name' for select * from constraint_name_test order by 1;
close 'constraint_name';
end;

--关键字带反引号-合理报错
start transaction;
cursor `constraint_name` for select * from constraint_name_test order by 1;
close `constraint_name`;
end;

--清理环境
drop table if exists constraint_name_test cascade;
