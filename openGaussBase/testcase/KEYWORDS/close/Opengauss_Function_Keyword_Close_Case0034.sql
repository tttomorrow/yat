--  @testpoint:opengauss关键字close(非保留)，作为游标名
--前置条件
drop table if exists close_test cascade;
create table close_test(cid int,fid int);

--关键字不带引号-成功
start transaction;
cursor close for select * from close_test order by 1;
close close;
end;

--关键字带双引号-成功
start transaction;
cursor "close" for select * from close_test order by 1;
close "close";
end;

--关键字带单引号-合理报错
start transaction;
cursor 'close' for select * from close_test order by 1;
close 'close';
end;

--关键字带反引号-合理报错
start transaction;
cursor `close` for select * from close_test order by 1;
close `close`;
end;

--清理环境
drop table close_test;