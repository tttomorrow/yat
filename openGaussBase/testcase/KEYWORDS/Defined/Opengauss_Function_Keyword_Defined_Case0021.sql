-- @testpoint: opengauss关键字defined(非保留)，作为函数名 带单引号、反引号时 合理报错

--关键字不带引号-成功
drop function if exists defined(i integer);
create function defined(i integer)
returns integer
as $$
begin
    return i+1;
end;
$$ language plpgsql;
/
select defined(3);

--清理环境
drop function defined(i integer);

--关键字带双引号-成功
drop function if exists "defined"(i integer);
create function "defined"(i integer)
returns integer
as $$
begin
    return i+1;
end;
$$ language plpgsql;
/

select "defined"(3);
--清理环境
drop function "defined"(i integer);

--关键字带单引号-合理报错
drop function if exists 'defined';
create function 'defined'(i integer)
returns integer
as $$
begin
    return i+1;
end;
$$ language plpgsql;
/

--关键字带反引号-合理报错
drop function if exists `defined`;
create function `defined`(i integer)
returns integer
as $$
begin
    return i+1;
end;
$$ language plpgsql;
/