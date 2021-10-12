-- @testpoint: opengauss关键字prepared(非保留)，作为游标名,合理报错

--前置条件
drop table if exists prepared_test cascade;
create table prepared_test(cid int,fid int);

--关键字不带引号-成功
start transaction;
cursor prepared for select * from prepared_test order by 1;
close prepared;
end;

--关键字带双引号-成功
start transaction;
cursor "prepared" for select * from prepared_test order by 1;
close "prepared";
end;

--关键字带单引号-合理报错
start transaction;
cursor 'prepared' for select * from prepared_test order by 1;
close 'prepared';
end;

--关键字带反引号-合理报错
start transaction;
cursor `prepared` for select * from prepared_test order by 1;
close `prepared`;
end;

--清理环境
drop table if exists prepared_test cascade;