-- @testpoint: opengauss关键字constraint_schema(非保留)，作为游标名，部分测试点合理报错

--前置条件
drop table if exists constraint_schema_test cascade;
create table constraint_schema_test(cid int,fid int);

--关键字不带引号-成功
start transaction;
cursor constraint_schema for select * from constraint_schema_test order by 1;
close constraint_schema;
end;

--关键字带双引号-成功
start transaction;
cursor "constraint_schema" for select * from constraint_schema_test order by 1;
close "constraint_schema";
end;

--关键字带单引号-合理报错
start transaction;
cursor 'constraint_schema' for select * from constraint_schema_test order by 1;
close 'constraint_schema';
end;

--关键字带反引号-合理报错
start transaction;
cursor `constraint_schema` for select * from constraint_schema_test order by 1;
close `constraint_schema`;
end;

--清理环境
drop table if exists constraint_schema_test cascade;
