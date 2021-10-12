-- @testpoint: opengauss关键字data(非保留)，作为游标名，部分测试点合理报错

--前置条件
drop table if exists data_test cascade;
create table data_test(cid int,fid int);

--关键字不带引号-成功
start transaction;
cursor data for select * from data_test order by 1;
close data;
end;

--关键字带双引号-成功
start transaction;
cursor "data" for select * from data_test order by 1;
close "data";
end;

--关键字带单引号-合理报错
start transaction;
cursor 'data' for select * from data_test order by 1;
close 'data';
end;

--关键字带反引号-合理报错
start transaction;
cursor `data` for select * from data_test order by 1;
close `data`;
end;
drop table if exists data_test cascade;
