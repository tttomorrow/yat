--  @testpoint:opengauss关键字nvarchar2(非保留)，作为函数名

--关键字不带引号
drop function if exists nvarchar2(i integer);
create function nvarchar2(i integer)
returns integer
as $$
begin
    return i+1;
end;
$$ language plpgsql;
/
--关键字带双引号
drop function if exists "nvarchar2"(i integer);
create function "nvarchar2"(i integer)
returns integer
as $$
begin
    return i+1;
end;
$$ language plpgsql;
/
drop function if exists "nvarchar2"(i integer);
--关键字带单引号-合理报错
drop function if exists 'nvarchar2'(i integer);
create function 'nvarchar2'(i integer)
returns integer
as $$
begin
    return i+1;
end;
$$ language plpgsql;
/
--关键字带反引号-合理报错
drop function if exists `nvarchar2`(i integer);
create function `nvarchar2`(i integer)
returns integer
as $$
begin
    return i+1;
end;
$$ language plpgsql;
/
