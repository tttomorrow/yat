-- @testpoint: opengauss关键字collation_name(非保留)，作为游标名，部分测试点合理报错

--前置条件
drop table if exists collation_name_test cascade;
create table collation_name_test(cid int,fid int);

--关键字不带引号-成功
start transaction;
cursor collation_name for select * from collation_name_test order by 1;
close collation_name;
end;

--关键字带双引号-成功
start transaction;
cursor "collation_name" for select * from collation_name_test order by 1;
close "collation_name";
end;

--关键字带单引号-合理报错
start transaction;
cursor 'collation_name' for select * from collation_name_test order by 1;
close 'collation_name';
end;

--关键字带反引号-合理报错
start transaction;
cursor `collation_name` for select * from collation_name_test order by 1;
close `collation_name`;
end;
drop table if exists collation_name_test cascade;