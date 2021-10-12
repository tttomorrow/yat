--  @testpoint:删除函数添加CASCADE参数并且省略函数参数
drop FUNCTION if EXISTS u_testfun92(int)  cascade;
CREATE FUNCTION u_testfun92 ( IN c_int int) RETURNS int  AS $$
        BEGIN
                RETURN (c_int);
        END;
$$ LANGUAGE plpgsql;
/

select proname from pg_proc where proname='u_testfun92';
--删除函数添加CASCADE参数并且省略函数参数类型（报错）
drop FUNCTION  u_testfun92 cascade;
--删除函数添加CASCADE参数并且添加函数参数类型（成功）
drop FUNCTION u_testfun92 (int) cascade;





