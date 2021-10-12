-- @testpoint: opengauss关键字mode(非保留)，作为函数名 带单引号、反引号时 合理报错

--关键字不带引号-成功
drop function if exists mode(i integer);
create function mode(i integer)
returns integer
as $$
begin
    return i+1;
end;
$$ language plpgsql;
/

--关键字带双引号-成功
drop function if exists "mode"(i integer);
create function "mode"(i integer)
returns integer
as $$
begin
    return i+1;
end;
$$ language plpgsql;
/

--关键字带单引号-合理报错
drop function if exists 'mode'(i integer);
create function 'mode'(i integer)
returns integer
as $$
begin
    return i+1;
end;
$$ language plpgsql;
/

--关键字带反引号-合理报错
drop function if exists `mode`(i integer);
create function `mode`(i integer)
returns integer
as $$
begin
    return i+1;
end;
$$ language plpgsql;
/
--清理环境
drop function if exists mode(integer);
drop function if exists "mode"(integer);