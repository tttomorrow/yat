-- @testpoint: opengauss关键字user(保留)，作为游标名，部分测试点合理报错

--前置条件
drop table if exists user_test cascade;
create table user_test(cid int,fid int);

--关键字不带引号-失败
start transaction;
cursor user for select * from user_test order by 1;
close user;
end;

--关键字带双引号-成功
start transaction;
cursor "user" for select * from user_test order by 1;
close "user";
end;

--关键字带单引号-合理报错
start transaction;
cursor 'user' for select * from user_test order by 1;
close 'user';
end;

--关键字带反引号-合理报错
start transaction;
cursor `user` for select * from user_test order by 1;
close `user`;
end;
drop table if exists user_test cascade;