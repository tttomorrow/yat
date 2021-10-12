--  @testpoint:opengauss关键字parameter_specific_schema(非保留)，作为用户组名


--关键字不带引号-成功
drop group if exists parameter_specific_schema;
create group parameter_specific_schema with password 'gauss@123';
drop group parameter_specific_schema;

--关键字带双引号-成功
drop group if exists "parameter_specific_schema";
create group "parameter_specific_schema" with password 'gauss@123';
drop group "parameter_specific_schema";

--关键字带单引号-合理报错
drop group if exists 'parameter_specific_schema';
create group 'parameter_specific_schema' with password 'gauss@123';

--关键字带反引号-合理报错
drop group if exists `parameter_specific_schema`;
create group `parameter_specific_schema` with password 'gauss@123';
