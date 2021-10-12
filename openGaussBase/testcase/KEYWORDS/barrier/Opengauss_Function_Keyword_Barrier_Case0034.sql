--  @testpoint:opengauss关键字barrier(非保留)，作为游标名
--前置条件
drop table if exists barrier_test cascade;
create table barrier_test(cid int,fid int);

--关键字不带引号-成功
start transaction;
cursor barrier for select * from barrier_test order by 1;
close barrier;
end;

--关键字带双引号-成功
start transaction;
cursor "barrier" for select * from barrier_test order by 1;
close "barrier";
end;

--关键字带单引号-合理报错
start transaction;
cursor 'barrier' for select * from barrier_test order by 1;
close 'barrier';
end;

--关键字带反引号-合理报错
start transaction;
cursor `barrier` for select * from barrier_test order by 1;
close `barrier`;
end;

--清理环境
drop table barrier_test;