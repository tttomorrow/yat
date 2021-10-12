--  @testpoint:opengauss关键字parameter_specific_schema(非保留)，作为角色名


--关键字不带引号-成功
drop role if exists parameter_specific_schema;
create role parameter_specific_schema with password 'gauss@123' valid until '2020-12-31';
drop role parameter_specific_schema;

--关键字带双引号-成功
drop role if exists "parameter_specific_schema";
create role "parameter_specific_schema" with password 'gauss@123' valid until '2020-12-31';
drop role "parameter_specific_schema";

--关键字带单引号-合理报错
drop role if exists 'parameter_specific_schema';
create role 'parameter_specific_schema' with password 'gauss@123' valid until '2020-12-31';

--关键字带反引号-合理报错
drop role if exists `parameter_specific_schema`;
create role `parameter_specific_schema` with password 'gauss@123' valid until '2020-12-31';
