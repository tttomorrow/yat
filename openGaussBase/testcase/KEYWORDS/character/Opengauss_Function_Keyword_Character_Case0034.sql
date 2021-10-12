--  @testpoint:opengauss关键字character(非保留)，作为游标名
--前置条件
drop table if exists character_test cascade;
create table character_test(cid int,fid int);

--关键字不带引号-成功
start transaction;
cursor character for select * from character_test order by 1;
close character;
end;

--关键字带双引号-成功
start transaction;
cursor "character" for select * from character_test order by 1;
close "character";
end;

--关键字带单引号-合理报错
start transaction;
cursor 'character' for select * from character_test order by 1;
close 'character';
end;

--关键字带反引号-合理报错
start transaction;
cursor `character` for select * from character_test order by 1;
close `character`;
end;

--清理环境
drop table character_test;