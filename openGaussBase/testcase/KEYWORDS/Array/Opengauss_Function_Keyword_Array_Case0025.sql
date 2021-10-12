--  @testpoint:opengauss关键字Array(保留)，作为角色名

--关键字不带引号-合理报错
drop role if exists Array;
create role Array with password 'gauss@123' valid until '2020-12-31';

--关键字带双引号-成功
drop role if exists "Array";
create role "Array" with password 'gauss@123' valid until '2020-12-31';

--清理环境
drop role "Array";

--关键字带单引号-合理报错
drop role if exists 'Array';
create role 'Array' with password 'gauss@123' valid until '2020-12-31';

--关键字带反引号-合理报错
drop role if exists `Array`;
create role `Array` with password 'gauss@123' valid until '2020-12-31';