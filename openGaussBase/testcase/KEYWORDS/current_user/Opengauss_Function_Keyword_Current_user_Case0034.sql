--  @testpoint:opengauss关键字current_user(保留)，作为游标名

--前置条件
drop table if exists current_user_test cascade;
create table current_user_test(cid int,fid int);

--关键字不带引号-失败
start transaction;
cursor current_user for select * from current_user_test order by 1;
close current_user;
end;

--关键字带双引号-成功
start transaction;
cursor "current_user" for select * from current_user_test order by 1;
close "current_user";
end;

--关键字带单引号-合理报错
start transaction;
cursor 'current_user' for select * from current_user_test order by 1;
close 'current_user';
end;

--关键字带反引号-合理报错
start transaction;
cursor `current_user` for select * from current_user_test order by 1;
close `current_user`;
end;

--清理环境
drop table current_user_test cascade;