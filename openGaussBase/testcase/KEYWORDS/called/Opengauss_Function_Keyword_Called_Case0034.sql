--  @testpoint:opengauss关键字called(非保留)，作为游标名
--前置条件
drop table if exists called_test cascade;
create table called_test(cid int,fid int);

--关键字不带引号-成功
start transaction;
cursor called for select * from called_test order by 1;
close called;
end;

--关键字带双引号-成功
start transaction;
cursor "called" for select * from called_test order by 1;
close "called";
end;

--关键字带单引号-合理报错
start transaction;
cursor 'called' for select * from called_test order by 1;
close 'called';
end;

--关键字带反引号-合理报错
start transaction;
cursor `called` for select * from called_test order by 1;
close `called`;
end;

--清理环境
drop table called_test;