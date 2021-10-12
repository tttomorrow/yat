-- @testpoint: opengauss关键字collation_schema(非保留)，作为用户组名 合理报错


--关键字不带引号-成功
drop group if exists collation_schema;
create group collation_schema with password 'haha@123';
drop group collation_schema;

--关键字带双引号-成功
drop group if exists "collation_schema";
create group "collation_schema" with password 'haha@123';
drop group "collation_schema";

--关键字带单引号-合理报错
drop group if exists 'collation_schema';
create group 'collation_schema' with password 'haha@123';

--关键字带反引号-合理报错
drop group if exists `collation_schema`;
create group `collation_schema` with password 'haha@123';

