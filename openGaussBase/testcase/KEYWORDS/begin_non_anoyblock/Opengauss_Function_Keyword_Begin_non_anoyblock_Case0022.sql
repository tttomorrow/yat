--  @testpoint:opengauss关键字begin_non_anoyblock(非保留)，作为用户组名
--关键字不带引号-成功
drop group if exists begin_non_anoyblock;
create group begin_non_anoyblock with password 'gauss@123';
drop group begin_non_anoyblock;

--关键字带双引号-成功
drop group if exists "begin_non_anoyblock";
create group "begin_non_anoyblock" with password 'gauss@123';
drop group "begin_non_anoyblock";

--关键字带单引号-合理报错
drop group if exists 'begin_non_anoyblock';

--关键字带反引号-合理报错
drop group if exists `begin_non_anoyblock`;
