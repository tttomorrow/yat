-- @testpoint: opengauss关键字Language(非保留)，作为函数名,部分测试点合理报错

--关键字不带引号-成功
drop function if exists Language;
create function Language(i integer)
returns integer
as $$
begin
    return i+1;
end;
$$ language plpgsql;
/
--关键字带双引号-成功
drop function if exists "Language";
create function "Language"(i integer)
returns integer
as $$
begin
    return i+1;
end;
$$ language plpgsql;
/
--关键字带单引号-合理报错
drop function if exists 'Language';
create function 'Language'(i integer)
returns integer
as $$
begin
    return i+1;
end;
$$ language plpgsql;
/
--关键字带反引号-合理报错
drop function if exists `Language`;
create function `Language`(i integer)
returns integer
as $$
begin
    return i+1;
end;
$$ language plpgsql;
/
--清理环境
drop function if exists language(integer);
drop function if exists "Language"(integer);