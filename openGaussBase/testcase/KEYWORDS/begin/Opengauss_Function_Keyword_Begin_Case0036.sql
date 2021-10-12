-- @testpoint: 用在存储过程中
drop table if exists T_PROvbnC_temp_18 ;
create table T_PROvbnC_temp_18
(
c_int int primary key,
c_number number,
c_varchar varchar(80),
c_date date
);



insert into T_PROvbnC_temp_18 values(3,3.12345,'   红绿灯','2018-8-8');

CREATE OR REPLACE PROCEDURE PROC_DML_TRUNCATE_PROC_18()
IS
v_refcur1 sys_refcursor;
c_cur1 date :='2018-8-8';
b_sql varchar(100);
BEGIN
				execute immediate '
				BEGIN
				open :1 for select c_date from #T_PROvbnC_temp_18 where c_date=c_cur1;
				dbms_sql.return_result(v_refcur1);
				END'using v_refcur1 ;

END;
/
drop table if exists t_provbnc_temp_18;
drop procedure proc_dml_truncate_proc_18;