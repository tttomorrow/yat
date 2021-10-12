--  @testpoint:opengauss关键字foreign(保留)，作为游标名

--前置条件
drop table if exists foreign_test cascade;
create table foreign_test(cid int,fid int);

--关键字不带引号-失败
start transaction;
cursor foreign for select * from foreign_test order by 1;
close foreign;
end;

--关键字带双引号-成功
start transaction;
cursor "foreign" for select * from foreign_test order by 1;
close "foreign";
end;

--关键字带单引号-合理报错
start transaction;
cursor 'foreign' for select * from foreign_test order by 1;
close 'foreign';
end;

--关键字带反引号-合理报错
start transaction;
cursor `foreign` for select * from foreign_test order by 1;
close `foreign`;
end;

--清理环境
drop table foreign_test cascade;