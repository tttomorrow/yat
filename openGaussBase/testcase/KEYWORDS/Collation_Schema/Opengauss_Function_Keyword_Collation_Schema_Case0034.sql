-- @testpoint: opengauss关键字collation_schema(非保留)，作为游标名 合理报错

--前置条件
drop table if exists collation_schema_test cascade;
create table collation_schema_test(cid int,fid int);

--关键字不带引号-成功
start transaction;
cursor collation_schema for select * from collation_schema_test order by 1;
close collation_schema;
end;

--关键字带双引号-成功
start transaction;
cursor "collation_schema" for select * from collation_schema_test order by 1;
close "collation_schema";
end;

--关键字带单引号-合理报错
start transaction;
cursor 'collation_schema' for select * from collation_schema_test order by 1;
close 'collation_schema';
end;

--关键字带反引号-合理报错
start transaction;
cursor `collation_schema` for select * from collation_schema_test order by 1;
close `collation_schema`;
end;
drop table if exists collation_schema_test cascade;