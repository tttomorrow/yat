--  @testpoint:opengauss关键字maxvalue(保留)，作为游标名

--前置条件
drop table if exists maxvalue_test cascade;
create table maxvalue_test(cid int,fid int);

--关键字不带引号-失败
start transaction;
cursor maxvalue for select * from maxvalue_test order by 1;
close maxvalue;
end;

--关键字带双引号-成功
start transaction;
cursor "maxvalue" for select * from maxvalue_test order by 1;
close "maxvalue";
end;

--关键字带单引号-合理报错
start transaction;
cursor 'maxvalue' for select * from maxvalue_test order by 1;
close 'maxvalue';
end;

--关键字带反引号-合理报错
start transaction;
cursor `maxvalue` for select * from maxvalue_test order by 1;
close `maxvalue`;
end;

--清理环境
drop table maxvalue_test cascade;