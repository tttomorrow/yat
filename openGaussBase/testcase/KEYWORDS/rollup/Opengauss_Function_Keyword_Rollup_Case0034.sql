--  @testpoint:opengauss关键字rollup(非保留)，作为游标名
--前置条件
drop table if exists rollup_test cascade;
create table rollup_test(cid int,fid int);

--关键字不带引号-成功
start transaction;
cursor rollup for select * from rollup_test order by 1;
close rollup;
end;

--关键字带双引号-成功
start transaction;
cursor "rollup" for select * from rollup_test order by 1;
close "rollup";
end;

--关键字带单引号-合理报错
start transaction;
cursor 'rollup' for select * from rollup_test order by 1;
close 'rollup';
end;

--关键字带反引号-合理报错
start transaction;
cursor `rollup` for select * from rollup_test order by 1;
close `rollup`;
end;

--清理环境
drop table rollup_test;