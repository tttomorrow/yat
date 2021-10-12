--  @testpoint:opengauss关键字returns(非保留)，作为游标名
--前置条件
drop table if exists returns_test cascade;
create table returns_test(cid int,fid int);

--关键字不带引号-成功
start transaction;
cursor returns for select * from returns_test order by 1;
close returns;
end;

--关键字带双引号-成功
start transaction;
cursor "returns" for select * from returns_test order by 1;
close "returns";
end;

--关键字带单引号-合理报错
start transaction;
cursor 'returns' for select * from returns_test order by 1;
close 'returns';
end;

--关键字带反引号-合理报错
start transaction;
cursor `returns` for select * from returns_test order by 1;
close `returns`;
end;

--清理环境
drop table returns_test;